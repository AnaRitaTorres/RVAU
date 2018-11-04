using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using Vuforia;

public class LockObjects : MonoBehaviour {

	public Button lockButton;
	public GameObject chaiseLong;
	public GameObject basketball;
	public GameObject books;
	public Camera secondCamera;
	
		
	void Start () {
	
		lockButton.onClick.AddListener(LockInPlace);

	}

	public string IdentifyTag() {

		var object_tag1 = GameObject.FindWithTag("Chaise").name;
		var object_tag2 = GameObject.FindWithTag("Book").name;
		var object_tag3 = GameObject.FindWithTag("Basketball").name;
		
		if (object_tag1 != null)
			return object_tag1;
		else if(object_tag2 != null)
			return object_tag2;
		else if(object_tag3 != null)
			return object_tag3;
		else
			return null;
		
	}

	
	void LockInPlace() {

		string objectToPlace = IdentifyTag();
		Debug.Log(objectToPlace);
		//after obtaining tracked object, permit only one lock of each kind
		
		var newChaise = Instantiate(chaiseLong, chaiseLong.transform.position, chaiseLong.transform.rotation);
		newChaise.transform.parent = secondCamera.transform;
		newChaise.transform.localScale =  new Vector3(5, 5, 5);
		newChaise.transform.localPosition = new Vector3(newChaise.transform.position.x, 0.0f, -newChaise.transform.position.z);
		
		var newBasketball = Instantiate(basketball, basketball.transform.position, basketball.transform.rotation);
		newBasketball.transform.parent = secondCamera.transform;
		newBasketball.transform.localScale =  new Vector3(5, 5, 5);
		newBasketball.transform.localPosition = new Vector3(newBasketball.transform.position.x, 0.0f, -newBasketball.transform.position.z);

		var newBooks = Instantiate(books, books.transform.position, books.transform.rotation);
		newBooks.transform.parent = secondCamera.transform;
		newBooks.transform.localScale =  new Vector3(5, 5, 5);
	 	newBooks.transform.localPosition = new Vector3(newBooks.transform.position.x, 0.0f, -newBooks.transform.position.z);
	}

	// Update is called once per frame
	void Update () {
		
	}
}
