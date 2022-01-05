import xadmin
from xadmin.views import BaseAdminPlugin,ListAdminView
from django.template import loader
from xadmin.plugins.utils import get_context_dict
#excel导入:
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False
    #返回为True时才加载插件
    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)
    def block_top_toolbar(self,context,nodes):
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html',context=get_context_dict(context)))
        # nodes.append(loader.render_to_string('xadmin/blocks/model_list.top_toolbar.exports.html',
        #                                      context=get_context_dict(context)))

xadmin.site.register_plugin(ListImportExcelPlugin,ListAdminView)
