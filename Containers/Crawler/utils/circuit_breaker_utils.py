import grpc
from circuit_breaker_pb2 import CircuitBreakerStatusRequest, CircuitBreakerStatus
from circuit_breaker_pb2_grpc import CircuitBreakerStub
from utils.logger import logger

class CircuitBreaker:
    def __init__(self, host, threshold, recovery):
        """
        Inizializza il Circuit Breaker.
        :param host: Servizio target da monitorare.
        :param threshold: Numero massimo di fallimenti consentiti.
        :param recovery: Tempo di recupero in secondi.
        """
        self.stub = self._get_stub(host)
        self.request = CircuitBreakerStatusRequest(
            host=host,
            threshold=threshold,
            recovery=recovery
        )

    def _get_stub(self, host):
        """
        Restituisce lo stub gRPC per comunicare con il Circuit Breaker.
        """
        channel = grpc.insecure_channel(host)
        return CircuitBreakerStub(channel)

    def assert_closed_or_half_open(self):
        """
        Controlla che il Circuit Breaker sia nello stato `CLOSED` o `HALF_OPEN`.
        Lancia un'eccezione se è `OPEN`.
        """
        response = self.stub.status(self.request)
        logger.info(f"Circuit Breaker status: {response.status}")
        if response.status == CircuitBreakerStatus.CircuitBreaker_OPEN:
            raise Exception("Circuit Breaker is OPEN. Blocking request.")

    def report_success(self):
        """
        Segnala un'operazione riuscita al Circuit Breaker.
        """
        try:
            self.stub.success(self.request)
            logger.info("Segnalato successo al Circuit Breaker.")
        except Exception as e:
            logger.error(f"Errore durante la segnalazione di successo: {e}")

    def report_failure(self):
        """
        Segnala un fallimento al Circuit Breaker.
        """
        try:
            self.stub.failure(self.request)
            logger.info("Segnalato fallimento al Circuit Breaker.")
        except Exception as e:
            logger.error(f"Errore durante la segnalazione di fallimento: {e}")
