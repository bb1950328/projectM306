# coding=utf-8
from django.shortcuts import render


def index(request):
    context = {
        "user": {"firstName": "Basil",
                 "lastName": "Bader"},
        "days": [{"id": "day1",
                  "displayName": "Do, 31.10.2019",
                  "entries": [{"id": "entry1",
                               "project_nr": 1,
                               "von": "7:23",
                               "bis": "11:54"},
                              {"id": "entry2",
                               "project_nr": 3,
                               "von": "12:27",
                               "bis": "16:25"},
                              ]
                  },
                 {"id": "day2",
                  "displayName": "Fr, 1.11.2019",
                  "entries": [{"id": "entry3",
                               "project_nr": 1,
                               "von": "7:26",
                               "bis": "11:51"},
                              {"id": "entry4",
                               "project_nr": 5,
                               "von": "12:20",
                               "bis": "15:55"},
                              ]
                  }
                 ]
    }
    return render(request, "index.html", context)
