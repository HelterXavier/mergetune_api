class NoBulkActionsMixin:
    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.clear()
        return actions

    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        if 'action_checkbox' in list_display:
            list_display.remove('action_checkbox')
        return list_display
