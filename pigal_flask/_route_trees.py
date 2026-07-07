
class RouteTree:

    def __init__(self):
        self.root = RouteNode()


    @property
    def routes(self):
        routes = {}
        self._collect(self.root, "", routes)
        return routes


    def clear(self):
        self.root = RouteNode()


    def add(self, route, template):
        node = self.root
        for segment in self._segments(route):
            print('add', segment)

            #
            # <path:path>
            #
            if segment.startswith("<path:"):
                print('got catch all')
                name = segment[6:-1]
                if node.catch_all is None:
                    node.catch_all = RouteNode(segment)
                    node.catch_all_name = name
                node = node.catch_all
                break

            #
            # <id>
            #
            elif segment.startswith("["):
                print('got dynamic')
                name = segment[1:-1]
                if node.parameter is None:
                    node.parameter = RouteNode(segment)
                    node.parameter_name = name

                elif node.parameter_name != name:
                    raise ValueError(
                        f"Conflicting parameter names "
                        f"'{node.parameter_name}' "
                        f"and '{name}'"
                    )
                node = node.parameter

            #
            # static
            #
            else:
                print('got static')
                if segment not in node.children:
                    node.children[segment] = RouteNode(segment)
                node = node.children[segment]

        if node.template is not None:
            raise ValueError(f"Duplicate route '{route}'")
        node.template = template


    def remove(self, route):
        stack = []
        node = self.root
        for segment in self._segments(route):
            stack.append((node, segment))
            if segment.startswith("<path:"):
                node = node.catch_all
            elif segment.startswith("<"):
                node = node.parameter
            else:
                node = node.children.get(segment)

            if node is None:
                return
        node.template = None


    def resolve(self, route):
        node = self.root
        for segment in self._segments(route):
            node = node.children.get(segment)
            if node is None:
                raise KeyError(route)

        if node.template is None:
            raise KeyError(route)
        return node.template


    def match(self, route):
        params = {}
        node = self.root
        segments = self._segments(route)

        i = 0
        while i < len(segments):
            segment = segments[i]

            #
            # priorité au statique
            #
            child = node.children.get(segment)
            if child is not None:
                node = child
                i += 1
                continue
            
            #
            # paramètre
            #
            if node.parameter is not None:
                params[node.parameter_name] = segment
                node = node.parameter
                i += 1
                continue

            #
            # catch all
            3
            if node.catch_all is not None:
                params[node.catch_all_name] = "/".join(segments[i:])
                node = node.catch_all
                i = len(segments)
                break
            raise KeyError(route)

        if node.template is None:
            raise KeyError(route)
        return node.template, params


    def _segments(self, route):
        route = route.strip("/")
        if route == "":
            return []
        return route.split("/")


    def _collect(self, node, prefix, routes):
        if node.template is not None:
            routes[prefix or "/"] = node.template

        #
        # statiques
        #
        for child in node.children.values():
            self._collect(
                child,
                prefix + "/" + child.segment,
                routes,
            )

        #
        # paramètre
        #
        if node.parameter is not None:
            self._collect(
                node.parameter,
                prefix + "/" + node.parameter.segment,
                routes,
            )

        #
        # catch all
        #
        if node.catch_all is not None:
            self._collect(
                node.catch_all,
                prefix + "/" + node.catch_all.segment,
                routes,
            )


class RouteNode:
    
    def __init__(self, segment=""):
        self.segment = segment
        
        # enfants statiques
        self.children = {}

        # enfant dynamique : <id>
        self.parameter = None
        self.parameter_name = None

        # enfant catch-all : <path:path>
        self.catch_all = None
        self.catch_all_name = None

        # template associé à ce noeud
        self.template = None
