﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EndLevel : MonoBehaviour {

	public GameObject blue;
	public Play scr;

	void Start () {}
	
	void OnTriggerEnter(Collider other)
    {
       if (other.gameObject == blue){
		   scr.EndLevel();
	   }
    }
}
