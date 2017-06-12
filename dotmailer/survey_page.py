from dotmailer import Base
from dotmailer.survey_fields import SurveyField


class SurveyPage(Base):

    name = None
    fields = []

    def __init__(self, **kwargs):

        fields = kwargs.pop('fields', [])
        for entry in fields:
            if isinstance(entry, SurveyField):
                self.fields.append(entry)
            elif isinstance(entry, dict):
                self.fields.append(SurveyField(**entry))
            else:
                # TODO: Work out what to do if something else is found
                pass
        super(SurveyPage, self).__init__(**kwargs)
