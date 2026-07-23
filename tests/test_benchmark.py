import time


def test_benchmark_suite():
    from benchmark.performance import BenchmarkSuite
    suite = BenchmarkSuite()
    suite.executar("tarefa_a", lambda: time.sleep(0.01))
    suite.executar("tarefa_b", lambda: sum(range(1000)))
    r = suite.relatorio()
    assert len(r) == 2
    assert suite.tempo_total() > 0