# coding=utf-8
import traceback

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from time_entry.model import admin as model_admin, importexport
from time_entry.view import base_view


def admin(request: WSGIRequest):
    con = {
        **base_view.get_user_context(request),
        "git_log": model_admin.get_git_log(),
        "import_options": importexport.get_all_exported_folders(),
    }
    return render(request, "admin.html", context=con)


def git_pull(request: WSGIRequest):
    success, output = model_admin.git_pull()
    msg = f"git pull wurde {'' if success else 'nicht '} erfolgreich durchgeführt.\n"
    return HttpResponse(msg + output, "text/plain")


def import_(request: WSGIRequest):
    folder = request.GET.get("folder")
    try:
        importexport.import_all_files(folder)
    except Exception as e:
        msg = "".join(map(str, e.args))
        traceback.print_exc()
    else:
        msg = "Import wurde erfolgreich durchgeführt."
    return HttpResponse(msg, "text/plain")


def export(request: WSGIRequest):
    folder = request.GET.get("folder")
    try:
        importexport.export_all_tables(folder)
    except Exception as e:
        msg = "".join(map(str, e.args))
        traceback.print_exc()
    else:
        msg = "Export wurde erfolgreich durchgeführt."
    return HttpResponse(msg, "text/plain")
