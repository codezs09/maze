from .searcher import Searcher
from .searcher_bfs import SearcherBFS
# from .searcher_dfs import SearcherDFS
from .searcher_dijkstra import SearcherDijkstra
from .searcher_a_star import SearcherAStar

class SearcherFactory:
    @staticmethod
    def create_searcher(searcher_type: str) -> Searcher:
        if searcher_type.lower() == "bfs":
            return SearcherBFS()
        # elif searcher_type.lower() == "dfs":
        #     return SearcherDFS()
        elif searcher_type.lower() == "dijkstra":
            return SearcherDijkstra()
        elif searcher_type.lower() == "a_star":
            return SearcherAStar()
        else:
            raise ValueError(f"Unknown searcher type: {searcher_type}")
