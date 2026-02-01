"""
Task Tracker Service
====================
Manages background task status for async operations like Magic Setup.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import uuid4
from threading import Lock
import json

# Thread-safe task storage
_tasks: Dict[str, Dict[str, Any]] = {}
_lock = Lock()


class TaskStatus:
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"


def create_task(task_type: str, metadata: Dict = None) -> str:
    """Create a new task and return its ID."""
    task_id = str(uuid4())
    
    with _lock:
        _tasks[task_id] = {
            "id": task_id,
            "type": task_type,
            "status": TaskStatus.PENDING,
            "progress": 0,
            "current_step": "Initializing...",
            "steps_completed": [],
            "result": None,
            "error": None,
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
    
    return task_id


def update_task(
    task_id: str,
    status: Optional[str] = None,
    progress: Optional[int] = None,
    current_step: Optional[str] = None,
    step_complete: Optional[str] = None,
    result: Optional[Dict] = None,
    error: Optional[str] = None
):
    """Update task progress."""
    with _lock:
        if task_id not in _tasks:
            return
        
        task = _tasks[task_id]
        
        if status:
            task["status"] = status
        if progress is not None:
            task["progress"] = progress
        if current_step:
            task["current_step"] = current_step
        if step_complete:
            task["steps_completed"].append({
                "step": step_complete,
                "status": "complete",
                "timestamp": datetime.utcnow().isoformat()
            })
        if result is not None:
            task["result"] = result
        if error:
            task["error"] = error
            task["status"] = TaskStatus.FAILED
        
        task["updated_at"] = datetime.utcnow().isoformat()


def get_task(task_id: str) -> Optional[Dict]:
    """Get task status."""
    with _lock:
        return _tasks.get(task_id, {}).copy() if task_id in _tasks else None


def get_all_tasks(limit: int = 50) -> List[Dict]:
    """Get recent tasks."""
    with _lock:
        tasks = list(_tasks.values())
        # Sort by created_at descending
        tasks.sort(key=lambda x: x["created_at"], reverse=True)
        return [t.copy() for t in tasks[:limit]]


def cleanup_old_tasks(max_age_hours: int = 24):
    """Remove tasks older than max_age_hours."""
    cutoff = datetime.utcnow().timestamp() - (max_age_hours * 3600)
    
    with _lock:
        to_delete = []
        for task_id, task in _tasks.items():
            try:
                created = datetime.fromisoformat(task["created_at"]).timestamp()
                if created < cutoff:
                    to_delete.append(task_id)
            except:
                pass
        
        for task_id in to_delete:
            del _tasks[task_id]
