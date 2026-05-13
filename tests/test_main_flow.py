import unittest
from unittest.mock import patch, MagicMock

class TestMainExecutionFlow(unittest.TestCase):

    @patch("visualization.drawGraph.G_draw")
    @patch("export.writeGraph.G_write_dot")
    @patch("generation.generateGraph.gen")
    def test_full_pipeline(
        self,
        mock_gen,
        mock_write,
        mock_draw
    ):
        """
        Проверяет полный сценарий:
        1. gen.gen(graph_title)
        2. w.G_write_dot(G, graph_title)
        3. d.G_draw(graph_title)
        """

        graph_title = "Barabasi-Albert"
        fake_graph = MagicMock()
        mock_gen.return_value = fake_graph

        import generation.generateGraph as gen
        import export.writeGraph as w
        import visualization.drawGraph as d

        G = gen.gen(graph_title)
        w.G_write_dot(G, graph_title)
        d.G_draw(graph_title)

        mock_gen.assert_called_once_with(graph_title)
        mock_write.assert_called_once_with(fake_graph, graph_title)
        mock_draw.assert_called_once_with(graph_title)


if __name__ == "__main__":
    unittest.main()