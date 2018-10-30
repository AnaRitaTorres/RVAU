﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using UnityEngine.UI;

public class LockObjects : MonoBehaviour {

	public Button lockButton;
	public GameObject chaiseLong;
	public GameObject basketball;
	public GameObject books;
	public GameObject camera;
	
	void Start () {
		lockButton.onClick.AddListener(LockInPlace);	
	}
	
	void LockInPlace(){

		// This makes it so there are many chaise longues... We might wanna change this
		// TODO
		var newChaise = Instantiate(chaiseLong, chaiseLong.transform.position, chaiseLong.transform.rotation);
		newChaise.transform.parent = camera.transform;
		newChaise.transform.localPosition = new Vector3(newChaise.transform.position.x, -newChaise.transform.position.y, 0.0f);
		newChaise.transform.localScale =  new Vector3(5, 5, 5);
		
		
	}

	// Update is called once per frame
	void Update () {
		
	}
}
