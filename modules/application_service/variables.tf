variable "connection_string_tpl"{
    description = "Nombre de la conexion para los servicios"
    type = string
    default = ""
}
variable "deployment_id" {
  description = "ID de despliegue global generado en tiempo de ejecución"
  type        = string
}

