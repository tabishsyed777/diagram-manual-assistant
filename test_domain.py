import unittest
import core

class DomainTests(unittest.TestCase):
    def test_cycle(self):
        a,b=core.read(core.DEFAULT)[:2]
        cycle={**b,"end":a["start"]}
        self.assertIsNone(core.answer([a,cycle],"path from hopper to absent in figure 1")["answer"])

    def test_figure_scope(self):
        self.assertIsNone(core.answer(core.read(core.DEFAULT),"what follows hopper in figure 2")["answer"])

    def test_challenge_queries(self):
        rows=core.validate(core.read(core.DEFAULT))
        for query,expected in core.read(core.DEFAULT.parent.parent/"qa/challenge.json"):
            with self.subTest(query=query):
                self.assertEqual(core.answer(rows,query)["answer"],expected)

    def test_import_svg(self):
        import import_figure
        self.assertEqual(import_figure.convert(core.DEFAULT.with_name("manual.svg")),core.read(core.DEFAULT))
