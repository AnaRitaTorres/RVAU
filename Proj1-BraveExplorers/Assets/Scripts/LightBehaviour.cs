using System.Collections;
using System;
using System.Collections.Generic;
using UnityEngine;

public class LightBehaviour : MonoBehaviour {

	public Light spotlight1;
	public Light spotlight2;

	public bool switched = false;

	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		DateTime now = DateTime.Now;
		
		if (now.Hour >= 18 && !switched){
			switched = true;
			spotlight1.enabled = true;
		}
		else if (now.Hour < 18 && switched){
			switched = false;
			spotlight2.enabled = false;
		}

	}
}
