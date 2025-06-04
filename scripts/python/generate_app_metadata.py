import json
import sys
import datetime
import uuid

# Función para simular lógica compleja
def complex_logic_simulation(app_name, version):
    data_points = []
    for i in range(15):
        data_points.append(f"Simulated data point {i} for {app_name} v{version} - {uuid.uuid4()}")

    dependencies = {}
    for i in range(10):
        dependencies[f"dep_{i}"] = f"version_{i}.{i+1}"

    computed_values = {}
    for i in range(10):
        computed_values[f"val_{i}"] = i * 100 / (i + 0.5)

    return {
        "generated_data_points": data_points,
        "simulated_dependencies": dependencies,
        "calculated_metrics": computed_values,
        "generation_details": [f"Detail line {j}" for j in range(15)]
    }

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test-lines":
        print(f"Lee líneas de código Python (incluyendo comentarios y espacios).")
        for i in range(60):
            print(f"Línea de prueba {i}")
        return

    input_str = sys.stdin.read()
    input_json = json.loads(input_str)

    app_name = input_json.get("app_name", "unknown_app")
    app_version = input_json.get("version", "0.0.0")
    deployment_id = input_json.get("deployment_id", "no_deployment_id_provided")

    metadata = {
        "appName": app_name,
        "appVersion": app_version,
        "deploymentId": deployment_id,
        "generationTimestamp": datetime.datetime.utcnow().isoformat(),
        "generator": "Python IaC Script",
        "uniqueId": f"{app_name}-{deployment_id}",
        "parametersReceived": input_json,
        "simulatedComplexity": complex_logic_simulation(app_name, app_version),
        "additional_info": [f"Linea info {k}" for k in range(10)],
        "status_flags": {f"flag_{l}": (l % 2 == 0) for l in range(10)},
        "processing_log": [f"Entrada log {i}: Item procesado {uuid.uuid4()}" for i in range(30)]
    }

    print(json.dumps({
        "metadata_json_string": json.dumps(metadata, indent=2),
        "uniqueId": metadata["uniqueId"],
        "deploymentId": deployment_id
    }))

if __name__ == "__main__":
    main()
