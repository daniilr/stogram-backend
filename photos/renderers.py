from rest_framework.renderers import JSONRenderer


class JSONWithCodeRender(JSONRenderer):

    def render(self, *args, **kwargs):
        kwargs['data']['status'] = kwargs['renderer_context']['request']['status_code']
        super(JSONRenderer, self).render(*args, **kwargs)