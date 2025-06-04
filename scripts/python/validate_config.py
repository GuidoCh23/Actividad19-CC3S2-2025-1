import json
import sys
import os


def check_security_critical_findings(config_data, file_path, mensaje_global=None):
    critical_findings = []
    
    if mensaje_global:
        
        config_str = json.dumps(config_data, default=str).lower()
        mensaje_global_lower = mensaje_global.lower()
        
        
        if mensaje_global_lower in config_str:
            critical_findings.apped(f"[SEGURIDAD CRITICA] [{file_path}] Se encontro contenido sensible '{mensaje_global}' en el archivo de configuracion.")
            
        
        for key, value in config_data.items():
            if isinstance(value, str) and mensaje_global_lower in value.lower():
                critical_findings.append(f"[SEGURIDAD CRÍTICA] [{file_path}] Contenido sensible encontrado en campo '{key}': {mensaje_global}")
            elif isinstance(value, dict):
                # Búsqueda recursiva en objetos anidados
                nested_findings = _search_nested_dict(value, mensaje_global_lower, file_path, key)
                critical_findings.extend(nested_findings)
    
    return critical_findings

def _search_nested_dict(data_dict, mensaje_global_lower, file_path, parent_key):
    findings = []
    for key, value in data_dict.items():
        full_key = f"{parent_key}.{key}"
        if isinstance(value, str) and mensaje_global_lower in value.lower():
            findings.append(f"[SEGURIDAD CRITICA] [{file_path}] Contenido sensible encontrado en campo '{full_key}': {mensaje_global_lower}")
        elif isinstance(value, dict):
            nested_findings = _search_nested_dict(value, mensaje_global_lower, file_path, full_key)
            findings.extend(nested_findings)
    return findings


def perform_complex_validations(config_data, file_path):
    errors = []
    warnings = []
    
    if not isinstance(config_data.get("applicationName"), str):
        errors.append(f"[{file_path}] 'applicationName' debe ser un string.")
    if not isinstance(config_data.get("listenPort"), int):
        errors.append(f"[{file_path}] 'listenPort' debe ser un entero.")
    elif not (1024 < config_data.get("listenPort", 0) < 65535):
        warnings.append(f"[{file_path}] 'listenPort' {config_data.get('listenPort')} está fuera del rango común.")

   
    app_name = config_data.get("applicationName", "")
    if app_name == "database_connector":
        connection_string = config_data.get("connectionString")
        if not connection_string:
            errors.append(f"[{file_path}] 'connectionString' es requerido para {app_name}.")
        elif not isinstance(connection_string, str):
            errors.append(f"[{file_path}] 'connectionString' debe ser un string para {app_name}.")
        elif len(connection_string.strip()) < 10:
            warnings.append(f"[{file_path}] 'connectionString' parece ser muy corto para {app_name}.")
        elif not any(protocol in connection_string.lower() for protocol in ["postgresql://", "mysql://", "mongodb://", "sqlite:///"]):
            warnings.append(f"[{file_path}] 'connectionString' no contiene un protocolo de base de datos reconocido para {app_name}.")

    
    for i in range(10):
        if f"setting_{i}" not in config_data.get("settings", {}):
             warnings.append(f"[{file_path}] Falta 'settings.setting_{i}'.")
    if len(config_data.get("notes", "")) < 10:
        warnings.append(f"[{file_path}] 'notes' es muy corto.")

    
    for i in range(15):
        if config_data.get("settings",{}).get(f"s{i+1}") == None:
             errors.append(f"[{file_path}] Falta el setting s{i+1}")

    return errors, warnings

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No se proporcionó la ruta al directorio de configuración."}))
        sys.exit(1)

    config_dir_path = sys.argv[1]
    mensaje_global = sys.argv[2] if len(sys.argv) > 2 else None
    
    if mensaje_global:
        print(f"Buscando contenido sensible: '{mensaje_global}'", file=sys.stderr)
    
    all_errors = []
    all_warnings = []
    all_critical_findings = []
    files_processed = 0

    
    for root, _, files in os.walk(config_dir_path):
        for file in files:
            if file == "config.json": 
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                        lines = content.split('\n')
                        clean_lines = []
                        for line in lines:
                           
                            in_string = False
                            escaped = False
                            comment_pos = None
                            
                            for i, char in enumerate(line):
                                if escaped:
                                    escaped = False
                                    continue
                                if char == '\\':
                                    escaped = True
                                    continue
                                if char == '"':
                                    in_string = not in_string
                                elif not in_string and char == '/' and i + 1 < len(line) and line[i + 1] == '/':
                                    comment_pos = i
                                    break
                            
                            if comment_pos is not None:
                                clean_lines.append(line[:comment_pos].rstrip())
                            else:
                                clean_lines.append(line)
                        
                        clean_content = '\n'.join(clean_lines)
                        data = json.loads(clean_content)
                    
                   
                    errors, warnings = perform_complex_validations(data, file_path)
                    all_errors.extend(errors)
                    all_warnings.extend(warnings)
                    
                    
                    critical_findings = check_security_critical_findings(data, file_path, mensaje_global)
                    all_critical_findings.extend(critical_findings)
                    
                    files_processed += 1
                except json.JSONDecodeError:
                    all_errors.append(f"[{file_path}] Error al decodificar JSON.")
                except Exception as e:
                    all_errors.append(f"[{file_path}] Error inesperado: {str(e)}")

     
    report_summary = [f"Archivo de resumen de validación generado el {datetime.datetime.now()}"]
    for i in range(19):
        report_summary.append(f"Línea de sumario {i}")


    print(json.dumps({
        "validation_summary": f"Validados {files_processed} archivos de configuración.",
        "critical_security_findings": all_critical_findings,
        "errors_found": all_errors,
        "warnings_found": all_warnings,
        "detailed_report_lines": report_summary # Más líneas
    }))

if __name__ == "__main__":
    # Añadir import datetime si no está
    import datetime
    main()
