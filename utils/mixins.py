class HTMXTemplateMixin:
    def get_template_names(self, ):
        if self.request.htmx:
            return "includes/goods_list.html"
        else:
            return self.template_name


