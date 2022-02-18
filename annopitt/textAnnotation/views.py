from django.shortcuts import render

from django.http import HttpResponse
import os
from django.core.files import File
from django.conf import settings
from textAnnotation.models import Annotations
from textAnnotation.models import Subreddit
import random
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import csv



# from django.conf.settings import STATIC_URL
@csrf_exempt
def index(request):
    populate_db(request)
    populate_subrules(request)

    anno = random.choice(Annotations.objects.filter(annotated=False))
    sub = Subreddit.objects.get(name = anno.subreddit)

    print ("sub", sub.name)
    print ("author", anno.author)
    print ("text", anno.text)

    context = {
    "u_id" : anno.u_id, 
    "author" : anno.author,
    "permalink": "http://reddit.com" + anno.permalink,
    "subrules" : sub.subrules.split("@@@###@@@"),
    "text" : anno.text,
    "submission_text" : anno.submission_text,
    "parent_text" : anno.parent_text,
    "p1" : anno.p1,
    "p2" : anno.p2,
    "p3" : anno.p3,
    "p4" : anno.p4,
    "p5" : anno.p5
    }

    return render (request, "textAnnotation/index.html", context)

def populate_subrules(request):
    with open(os.path.join(settings.BASE_DIR, 'textAnnotation/static/annotation-files/subrules.tsv'), "r", encoding = "utf-8") as f:
        for line in f:
            row = line.strip().split("\t")
            if Subreddit.objects.filter(name=row[0]).exists():
                   print ("already exists ", row[0])
            else:
                newsub = Subreddit(name = row[0], subrules = row[1])
                newsub.save()
    return

def populate_db(request):
    print ("populating db")
    subfiles = os.listdir(os.path.join(settings.BASE_DIR, 'textAnnotation/static/annotation-files/subs/'))
    print (subfiles)
    for subfile in subfiles:
        count = 0
        with open(os.path.join(settings.BASE_DIR, 'textAnnotation/static/annotation-files/subs/' + subfile), "r", encoding = "utf-8") as f:
            for line in f:
                count += 1
                print (count)
                row = line.strip().split("\t")
                # row = [authors[i], u_ids[i], subreddits[i], subrules[i], texts[i], submission_texts[i], parent_texts[i], p1s[i], p2s[i], p3s[i], p4s[i], p5s[i]]
                if Annotations.objects.filter(u_id=row[1]).exists():
                   print ("already exists ", row[1])
                else:
                      ###do otherthing###
                    annotation = Annotations(author = row[0], u_id = row[1], subreddit = row[2], subrules = "", text = row[4], submission_text = row[5], parent_text = row[6], p1 = row[7], p2 = row[8], p3 = row[9], p4 = row[10], p5 = row[11], permalink = row[12])
                    annotation.save()
    return

@csrf_exempt
def export_db(request):
    fields = Annotations._meta.fields
    print (fields)
    with open(os.path.join(settings.BASE_DIR, "annotation-export.tsv"), 'w', encoding = "utf-8") as csvfile:
        # write your header first
        row = ""
        for field in fields:
            row += field.name + "\t"
        csvfile.write(row + "\n")
        
        for obj in Annotations.objects.all():
            row = ""
            for field in fields:
                 row += str(getattr(obj, field.name)) + "\t"
            csvfile.write(row + "\n")

    return redirect("/")


@csrf_exempt
def update_db(request):
    print (request)
    u_id = request.POST.get("u_id")
    print ("reddit rules broken", request.POST.getlist("redditrules"))
    print ("subrules broken", request.POST.getlist("subrules"))
    print ("check offensive", request.POST.getlist("offensive"))
    print ("check hate", request.POST.getlist("hate"))
    print ("check targets", request.POST.getlist("targets"))
    print ("check other", request.POST.get("other-target"))
    print ("target paraphrases", request.POST.getlist("parap"))


    update_anno = Annotations.objects.get(u_id = u_id)
    update_anno.redrules = "@@@***@@@".join(request.POST.getlist("redditrules"))
    update_anno.subrules = "@@@###@@@".join(request.POST.getlist("subrules"))
    update_anno.selection = "@@@&&&@@@".join(request.POST.getlist("parap"))
    update_anno.custom_p = request.POST.get("custom-paraphrase")
    update_anno.other = request.POST.get("other-target")
    update_anno.annotated = True

    if len(request.POST.getlist("skip")) > 0:
        update_anno.skip = True
    else:
        update_anno.skip = False

    if len(request.POST.getlist("context-helpful")) > 0:
        update_anno.context_helpful = 1
    else:
        update_anno.context_helpful = 0

    if len(request.POST.getlist("offensive")) > 0:
        update_anno.offensive = 1
    else:
        update_anno.offensive = 0
    if len(request.POST.getlist("hatespeech")) > 0:
        update_anno.hate_speech = 1
    else:
        update_anno.hate_speech = 0
    targets = request.POST.getlist("targets")
    if "Gender" in targets:
        update_anno.gender = 1
    else:
        update_anno.gender = 0

    if "Race/Ethnicity" in targets:
        update_anno.race = 1
    else:
        update_anno.race = 0

    if "Orientation" in targets:
        update_anno.orientation = 1
    else:
        update_anno.orientation = 0

    if "Religion" in targets:
        update_anno.religion = 1
    else:
        update_anno.religion = 0
    other_target = request.POST.get("other-target")
    update_anno.other = other_target

    update_anno.save()



    anno = random.choice(Annotations.objects.filter(annotated=False))
    sub = Subreddit.objects.get(name = anno.subreddit)

    print ("sub", sub.name)
    print ("author", anno.author)
    print ("text", anno.text)

    context = {
    "u_id" : anno.u_id, 
    "author" : anno.author,
    "subrules" : sub.subrules.split("@@@###@@@"),
    "text" : anno.text,
    "submission_text" : anno.submission_text,
    "parent_text" : anno.parent_text,
    "p1" : anno.p1,
    "p2" : anno.p2,
    "p3" : anno.p3,
    "p4" : anno.p4,
    "p5" : anno.p5
    }

    return redirect("/")

@csrf_exempt
def fetch_anno(request):
    annno = random.choice(Annotations.objects.filter(annotated=False))

    author = anno.author
    subrules = anno.subrules
    text = anno.text
    submission_text = anno.submission_text
    parent_text = anno.parent_text

    return 