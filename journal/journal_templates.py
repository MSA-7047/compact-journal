from journal.models import Template
def createTemplate():
    Template.objects.create(
                    title = "template 1",
                    description = "template summary 1",
                    bio = "this is the first template",
                )
    Template.objects.create(
                    title = "template 2",
                    description = "template summary 2",
                    bio = "this is the first template",
                )
    Template.objects.create(
                    title = "template 3",
                    description = "template summary 3",
                    bio = "this is the first template",
                )
    Template.objects.create(
                    title = "template 4",
                    description = "template summary 4",
                    bio = "this is the first template",
                )
    Template.objects.create(
                    title = "template 5",
                    description = "template summary 5",
                    bio = "this is the first template",
                )