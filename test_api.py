#!/usr/bin/env python
"""
Simple API testing script
Tests all major endpoints
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

def print_response(title, response):
    """Pretty print response"""
    print(f"\n{'='*60}")
    print(f"📍 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    if response.status_code == 204:
        print("No content (successful deletion)")
    else:
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)

def test_api():
    """Run API tests"""
    print("\n🧪 Testing PlanLLaMA API")
    print("=" * 60)
    
    # Test 1: Get all employees
    response = requests.get(f"{BASE_URL}/employees")
    print_response("GET /api/employees", response)
    
    # Test 2: Get PMs only
    response = requests.get(f"{BASE_URL}/employees?role=pm")
    print_response("GET /api/employees?role=pm", response)
    
    # Test 3: Get specific employee
    response = requests.get(f"{BASE_URL}/employees/e03")
    print_response("GET /api/employees/e03", response)
    
    # Test 4: Get employee workload
    response = requests.get(f"{BASE_URL}/employees/e03/workload")
    print_response("GET /api/employees/e03/workload", response)
    
    # Test 5: Get all projects
    response = requests.get(f"{BASE_URL}/projects")
    print_response("GET /api/projects", response)
    
    # Test 6: Get project with tasks
    response = requests.get(f"{BASE_URL}/projects/p01?include_tasks=true")
    print_response("GET /api/projects/p01?include_tasks=true", response)
    
    # Test 7: Get project members
    response = requests.get(f"{BASE_URL}/projects/p01/members")
    print_response("GET /api/projects/p01/members", response)
    
    # Test 8: Get project stats
    response = requests.get(f"{BASE_URL}/projects/p01/stats")
    print_response("GET /api/projects/p01/stats", response)
    
    # Test 9: Get all tasks (enriched)
    response = requests.get(f"{BASE_URL}/tasks?enrich=true")
    print_response("GET /api/tasks?enrich=true", response)
    
    # Test 10: Get tasks by status
    response = requests.get(f"{BASE_URL}/tasks?status=In Progress&enrich=true")
    print_response("GET /api/tasks?status=In Progress", response)
    
    # Test 11: Get tasks by assignee
    response = requests.get(f"{BASE_URL}/tasks/by-assignee/e03")
    print_response("GET /api/tasks/by-assignee/e03", response)
    
    # Test 12: Get tasks by project
    response = requests.get(f"{BASE_URL}/tasks/by-project/p01")
    print_response("GET /api/tasks/by-project/p01", response)
    
    # Test 13: Get task stats
    response = requests.get(f"{BASE_URL}/tasks/stats")
    print_response("GET /api/tasks/stats", response)
    
    # Test 14: Create new task
    new_task = {
        "task_id": "t99",
        "title": "Test Task",
        "description": "This is a test task",
        "project_id": "p01",
        "assignee_id": "e03",
        # Hata düzeltildi: 'dueDate' -> 'due_date'
        "due_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "priority": "medium",
        # Hata düzeltildi: 'estimatedHours' -> 'estimated_hours'
        "estimated_hours": 4
    }
    response = requests.post(f"{BASE_URL}/tasks", json=new_task)
    print_response("POST /api/tasks (Create)", response)
    
    # Test 15: Update task status
    response = requests.patch(
        f"{BASE_URL}/tasks/t99/status",
        json={"status": "In Progress"}
    )
    print_response("PATCH /api/tasks/t99/status", response)
    
    # Test 16: Update full task
    update_data = {
        "title": "Updated Test Task",
        "priority": "high",
        "estimated_hours": 6 # 'estimated_hours' olarak güncellendi
    }
    response = requests.put(f"{BASE_URL}/tasks/t99", json=update_data)
    print_response("PUT /api/tasks/t99 (Update)", response)
    
    # Test 17: Delete task
    response = requests.delete(f"{BASE_URL}/tasks/t99")
    print_response("DELETE /api/tasks/t99", response)
    
    print("\n✅ All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API")
        print("Make sure the server is running on http://localhost:5000")
    except Exception as e:
        print(f"\n❌ Error: {e}")
