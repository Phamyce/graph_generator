import unittest
from unittest.mock import patch, MagicMock

import generation.generateGraph as gen
import export.writeGraph as w
import visualization.drawGraph as d

class TestGenerateGraph(unittest.TestCase):

    def test_gen_returns_graph(self):
        """
        Проверяем, что gen.gen(graph_title)
        возвращает объект графа и не None
        """
        graph_title = "Barabasi-Albert"
        G = gen.gen(graph_title)

        self.assertIsNotNone(G)
        self.assertTrue(hasattr(G, "nodes"))
        self.assertTrue(hasattr(G, "edges"))


class TestWriteGraph(unittest.TestCase):

    @patch("networkx.drawing.nx_pydot.write_dot")
    def test_write_dot_called(self, mock_write_dot):
        """
        Проверяем, что write_dot вызывается корректно
        """
        fake_graph = MagicMock()
        graph_title = "Barabasi-Albert"

        w.G_write_dot(fake_graph, graph_title)

        mock_write_dot.assert_called_once()


class TestDrawGraph(unittest.TestCase):

    @patch("visualization.drawGraph.nx.nx_agraph.read_dot")
    @patch("visualization.drawGraph.plt.show")
    def test_draw_called(self, mock_show, mock_read_dot):
        """
        Проверяем, что граф читается и отображается
        """
        graph_title = "Barabasi-Albert"

        mock_graph = MagicMock()
        mock_read_dot.return_value = mock_graph

        d.G_draw(graph_title)

        mock_read_dot.assert_called_once()
        mock_show.assert_called_once()


if __name__ == "__main__":
    unittest.main()