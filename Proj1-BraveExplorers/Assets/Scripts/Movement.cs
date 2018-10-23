using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Movement : MonoBehaviour {

	public GameObject character;
	Rigidbody characterRigidBody; 
	
	public float speed = 10f;
	float directionX;

	void Start () {
		characterRigidBody = character.AddComponent<Rigidbody>();
		characterRigidBody.mass = 5;
	}
	
	void Update () {
		
	
		
		
	}
}
