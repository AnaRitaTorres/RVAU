using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using Vuforia;

public class LockObjects : MonoBehaviour {

	public Button lockButton;
	public Button undoButton;
	public GameObject chaiseLong;
	public GameObject books;
	public GameObject basketball;
	public GameObject exit;
	public GameObject trap;
	public Camera secondCamera;
	public List<Move> moves;

	public class Move {
		public GameObject obj;

		public Move(GameObject objct){
			obj = objct;
		}
	}

	void Start () { 
		moves = new List<Move>();
		lockButton.onClick.AddListener(LockInPlace);
		undoButton.onClick.AddListener(UndoMove);
	}

	private void LockObject(GameObject obj) {

		var container = new GameObject(obj.transform.name + " Container");

		container.transform.parent = secondCamera.transform;		
		container.transform.localPosition = obj.transform.localPosition;
		container.transform.position = obj.transform.position;
		container.transform.localScale = new Vector3(1,1,1);

		var delta = (Mathf.Abs(container.transform.localPosition.z) 
					* Mathf.Abs(container.transform.localPosition.x) 
					/ (800 - Mathf.Abs(container.transform.localPosition.z)));

		if (container.transform.localPosition.x < 0) delta = -delta;

		var newObject = Instantiate(obj, container.transform.position, obj.transform.rotation, container.transform);
		newObject.transform.localScale =  new Vector3(	obj.transform.localScale.x * obj.transform.parent.transform.localScale.x * (1 + 2*Mathf.Abs(delta)/800),
														obj.transform.localScale.y * obj.transform.parent.transform.localScale.y * (1 + 2*Mathf.Abs(delta)/800),
														obj.transform.localScale.z * obj.transform.parent.transform.localScale.z * (1 + 2*Mathf.Abs(delta)/800));
		container.transform.localPosition = new Vector3(container.transform.localPosition.x + delta, container.transform.localPosition.y,0);

		moves.Add(new Move(container));

	}

	private void UndoMove(){
		if (moves.Count != 0){
			var obj = moves[moves.Count - 1].obj;
			Destroy(obj);
			moves.RemoveAt(moves.Count - 1);
		}
	}

	void checkForLock(string objName, GameObject obj){
		if (GameObject.Find(obj.transform.name + " Container") != null) return;
		if (GameObject.Find(objName).GetComponent<Renderer>().isVisible){
			LockObject(obj);
		}
	}

	void LockInPlace() {
		checkForLock("ChaiseLong", chaiseLong);
		checkForLock("Basketball", basketball);
		checkForLock("book", books);
		checkForLock("Trap", trap);
		checkForLock("firedoor", exit);
	}
}
