param([string]$cmd="run")
switch ($cmd) {
  "run" { python manage.py runserver }
  "m"   { python manage.py migrate }
  "su"  { python manage.py createsuperuser }
  default { Write-Host "cmd: run|m|su" }
}