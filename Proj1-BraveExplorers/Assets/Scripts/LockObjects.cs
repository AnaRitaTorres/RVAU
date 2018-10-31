using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using UnityEngine.UI;

public class LockObjects : MonoBehaviour {

	public Button lockButton;
	public GameObject chaiseLong;
	public GameObject basketball;
	public GameObject books;
	public Camera secondCamera;
	//public GameObject blue;
	
	void Start () {
		lockButton.onClick.AddListener(LockInPlace);	
	}
	
	void LockInPlace(){

		// This makes it so there are many chaise longues... We might wanna change this
		// TODO
		var newChaise = Instantiate(chaiseLong, chaiseLong.transform.position, chaiseLong.transform.rotation);
		newChaise.transform.parent = secondCamera.transform;
		newChaise.transform.localScale =  new Vector3(5, 5, 5);
		newChaise.transform.localPosition = new Vector3(newChaise.transform.position.x, -newChaise.transform.position.y, 0.0f);
		
	}

	// Update is called once per frame
	void Update () {
		
	}
}
