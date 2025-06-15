{{- define "mongodb.labels" -}}
app.kubernetes.io/name: mongodb
app.kubernetes.io/instance: "{{ .Release.Name }}"
app.kubernetes.io/version: "{{ .Chart.AppVersion }}"
app.kubernetes.io/managed-by: "{{ .Release.Service }}"
app.kubernetes.io/component: {{ .Chart.Name }}
app.kubernetes.io/part-of: {{ .Release.Name }}
helm.sh/chart: "{{ .Chart.Name }}-{{ .Chart.Version }}"
{{- end -}}


{{- define "postgres.labels" -}}
app.kubernetes.io/name: postgres
app.kubernetes.io/instance: "{{ .Release.Name }}"
app.kubernetes.io/version: "{{ .Chart.AppVersion }}"
app.kubernetes.io/managed-by: "{{ .Release.Service }}"
app.kubernetes.io/component: {{ .Chart.Name }}
app.kubernetes.io/part-of: {{ .Release.Name }}
helm.sh/chart: "{{ .Chart.Name }}-{{ .Chart.Version }}"
{{- end -}}
