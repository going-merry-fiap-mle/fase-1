import threading
from http import HTTPStatus

from flask import Blueprint, Response, jsonify

from app.controller.scraping_controller import ScrapingController
from app.utils.logger import AppLogger
from app.utils.task_manager import TaskStatus, default_task_manager

scraper_bp = Blueprint("scraping", __name__, url_prefix="/api/v1/scraping")


logger = AppLogger(__name__)


def _scraping_worker(task_id: str) -> None:
    default_task_manager.set_status(task_id, TaskStatus.RUNNING, "started")
    try:
        controller = ScrapingController()
        controller.call_controller()
        default_task_manager.set_status(task_id, TaskStatus.SUCCESS, "completed")
        logger.info(f"Scraping task {task_id} completed", status=HTTPStatus.OK)
    except Exception as exc:
        logger.exception(f"Scraping task {task_id} failed: {exc}")
        default_task_manager.set_status(task_id, TaskStatus.ERROR, str(exc))


@scraper_bp.route("", methods=["GET"])
def scraping() -> tuple[Response, int]:
    """
    Realizar o web scraping dos livros
    ---
    tags:
      - Web Scraping
    responses:
        202:
            description: Scraping iniciado com sucesso com task id
    """
    task_id = default_task_manager.create_task()

    thread = threading.Thread(target=lambda: _scraping_worker(task_id))
    thread.daemon = True
    thread.start()

    return (
        jsonify({"message": "Scraping iniciado com sucesso", "task_id": task_id}),
        HTTPStatus.ACCEPTED,
    )


@scraper_bp.route("/status/<task_id>", methods=["GET"])
def scraping_status(task_id: str) -> tuple[Response, int]:
    """
    Consultar o status do scraping
    ---
    tags:
      - Web Scraping
    parameters:
      - name: task_id
        in: path
        type: string
        required: true
        description: UUID da tarefa de scraping
    responses:
      200:
        description: Status do scraping
        schema:
          type: object
          properties:
            task_id:
              type: string
    """
    task = default_task_manager.get_task(task_id)
    if task is None:
        return (
            jsonify({"message": "task not found", "task_id": task_id}),
            HTTPStatus.NOT_FOUND,
        )

    return (
        jsonify(
            {"task_id": task_id, "status": task["status"], "message": task["message"]}
        ),
        HTTPStatus.OK,
    )
