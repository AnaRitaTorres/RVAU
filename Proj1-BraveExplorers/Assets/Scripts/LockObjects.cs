using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using Vuforia;

public class LockObjects : MonoBehaviour {

	public Button lockButton;
	public GameObject gameObject;
	public Camera secondCamera;
	
	void Start () {
	
		lockButton.onClick.AddListener(LockInPlace);

	}

	public string IdentifyTag() {

		Debug.Log(gameObject.tag);
		return null;
		
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
		//Destroy(obj);

	}
	void LockInPlace() {
		Debug.Log(gameObject.tag);
		/* string objectToPlace = IdentifyTag();

		switch (objectToPlace) {
			case "ChaiseLong": {
				LockObject(chaiseLong);
				break;
			}
			case "Book": {
				LockObject(books);
				break;
			}
			case "Basketball": {
				LockObject(basketball);
				break;
			}
		}*/

		LockObject(gameObject);
	}

	// Update is called once per frame
	void Update () {
		
	}
}
