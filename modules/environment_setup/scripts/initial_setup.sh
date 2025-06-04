#!/bin/bash
ENV_NAME=$1
README_PATH=$2
CONTROL_FILE="placeholder_control.txt"
EXECUTION_COUNT_FILE="execution_count.txt"

echo "Ejecutando setup inicial para el entorno: $ENV_NAME"
echo "Fecha de setup: $(date)" > setup_log.txt
echo "Readme se encuentra en: $README_PATH" >> setup_log.txt

if [ ! -f "$CONTROL_FILE" ]; then
    echo "Archivo de control '$CONTROL_FILE' no encontrado. Realizando acciones de setup inicial..."
    echo "Creando archivo de placeholder unico..."
    touch placeholder_$(date +%s).txt 
    echo "Creando archivo de control: $CONTROL_FILE"
    touch "$CONTROL_FILE" 

    if [ ! -f "$EXECUTION_COUNT_FILE" ]; then
        echo "0" > "$EXECUTION_COUNT_FILE"
    fi
    CURRENT_COUNT=$(cat "$EXECUTION_COUNT_FILE")
    NEW_COUNT=$((CURRENT_COUNT + 1))
    echo "$NEW_COUNT" > "$EXECUTION_COUNT_FILE"
    echo "Contador de ejecucion incrementado a: $NEW_COUNT"

    echo "Setup inicial completado."

    for i in {1..20}; do
        echo "Paso de configuración simulado $i..." >> setup_log.txt
    done
else
    echo "Archivo de control '$CONTROL_FILE' ya existe. Omitiendo acciones de setup inicial."
    echo "Setup inicial omitido a las $(date)." >> setup_log.txt
fi