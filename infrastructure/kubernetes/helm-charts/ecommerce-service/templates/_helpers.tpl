{{/*
Expand the name of the chart.
*/}}
{{- define "ecommerce-service.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "ecommerce-service.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "ecommerce-service.labels" -}}
helm.sh/chart: {{ include "ecommerce-service.chart", . }}
{{ include("ecommerce-service.selectorLabels", .) }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "ecommerce-service.selectorLabels" -}}
app.kubernetes.io/name: {{ include("ecommerce-service.name", .) }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the service account name
*/}}
{{- define "ecommerce-service.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include("ecommerce-service.fullname", .)) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Fullname
*/}}
{{- define "ecommerce-service.fullname" -}}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
