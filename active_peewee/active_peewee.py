import peewee


class __ParseMeta(type):

    def __getattr__(self, method_name):
        """here is where the magic happens."""

        def inner(*args, **kwargs):
            return self.__parse(method_name, *args)

        inner.__name__ = method_name
        return inner

    def __parse(self, method_name, *args):
        fields_to_parse = method_name.replace('filter_by_', '').split('_')

        fd, op = [], []
        i = 0
        for part in fields_to_parse:
            if i % 2 == 0:  # eh field
                fd.append(part)
            else:  # eh operador
                op.append(part)

            i += 1

        query = {}
        if len(op) == 1:
            query['agregate'] = op[0]

        for idx, p in enumerate(args):
            query[fd[idx]] = {'operator': 'eq', 'value': p}

        return query


class ActiveMeta(__ParseMeta, peewee.BaseModel):
    pass
