from ibge_crawler.common import ibge_logger


"""
Recipe by Mateus Mercer ~ mateusmercer@gmail.com

This code is released with the MIT license, if you
didn't got a copy, get a copy at https://opensource.org/licenses/MIT

12/2016
"""


class DictClosured:
    def as_dict(self) -> dict:
        """
        Returns a dictionary with all functions closure levels inside a class.
        eg:

        class z(DictClosured):
            def x(self):
                def y(self):
                    return "I'm here"
                return y

        inst = z()

        inst.as_dict() will return a dictionary in a "json way" with the content as follows
        {
            "x":
            {
                "Y": "I'm here"
            }
        }
        """
        d = {}

        # Avoid protected funtions
        valid_functions = [
            getattr(self, attr)
            for attr in dir(self)
            if not attr.startswith("_")
            and attr is not "as_dict"
        ]

        # Avoid attributtes
        valid_functions = [attr for attr in valid_functions if callable(attr)]

        for func in valid_functions:
            self._recursive_closure(d, func)
        return d

    @staticmethod
    def _is_callable_list(funcs: list) -> bool:
        """
        Checks if ALL the members of a list are callable and returns true or false.
        """
        for func in funcs:
            if not callable(func):
                return False

        return True

    def _recursive_closure(self, dicto, func: callable):
        """
        The primary function of this class finds all the function and
        organize them in a dictionary inluding closure levels.
        """
        try:
            fname = func.__name__
        except AttributeError:
            fname = "!NO NAME!"

        data = None
        try:
            try:
                data = func()
            except TypeError:
                data = func(self)
        except Exception as e:
            ibge_logger.error("DICT CLOSURED ERROR! %s throwed an exception. "
                          "%s in %s." % (fname, str(e), self.__class__.__name__))
            data = None
        finally:
            dicto[fname] = data

        if type(data) is list and self._is_callable_list(data):
            dicto[fname] = {}
            for tfunc in data:
                self._recursive_closure(dicto[fname], tfunc)

        return dicto
