using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Movement : MonoBehaviour {

	public enum JumpStatus {Grounded, GoingUp, GoingDown};
	public enum MoveStatus {Grounded, MovingLeft, MovingRight};

	public GameObject character;
	public Button jumpButton;
	public JumpStatus jstatus = JumpStatus.Grounded;
	public MoveStatus mstatus = MoveStatus.Grounded;

	float jumpTime = 0.75f;
	float currTime = 0.0f;
	float currJumpSpeed = 0.0f;
	float currDirectionalSpeed = 0.0f;

	float savedMSpeed = 0.0f;
	float savedJSpeed = 0.0f;
	float savedJTime = 0.0f;
	bool paused = false;
			
	void Start () {
		jstatus = JumpStatus.Grounded;
		mstatus = MoveStatus.Grounded;
		jumpButton.onClick.AddListener(Jump);
	}
	
	public void MoveLeft(bool pressed) {
		
		if (mstatus == MoveStatus.Grounded && pressed){
			character.transform.Rotate(Vector3.up * 180, Space.Self); 
			mstatus = MoveStatus.MovingLeft;
			currDirectionalSpeed = 30f; 
		}
		else if (mstatus == MoveStatus.MovingLeft && !pressed) {
			character.transform.Rotate(Vector3.up * -180, Space.Self); 
			mstatus = MoveStatus.Grounded;
			currDirectionalSpeed = 0.0f;
		}
	}

	public void MoveRight(bool pressed) {
		if (mstatus == MoveStatus.Grounded && pressed){ 
			mstatus = MoveStatus.MovingRight;
			currDirectionalSpeed = 30f; 
		}
		else if (mstatus == MoveStatus.MovingRight && !pressed) {
			mstatus = MoveStatus.Grounded;
			currDirectionalSpeed = 0.0f;
		}
	}

	void Jump() {
		if (jstatus != JumpStatus.Grounded) return;
		else {
			jstatus = JumpStatus.GoingUp;
		}
	}

	public void PauseMovement(){
		savedMSpeed = currDirectionalSpeed;
		savedJSpeed = currJumpSpeed;
		savedJTime = currTime;

		currTime = 0.0f;
		currDirectionalSpeed = 0.0f;
		currJumpSpeed = 0.0f;
		
		paused = true;

		character.GetComponent<Rigidbody>().isKinematic = true;
	}

	public void ResumeMovement(){
		currDirectionalSpeed = savedMSpeed;
		currJumpSpeed = savedJSpeed;
		currTime = savedJTime;

		paused = false;

		character.GetComponent<Rigidbody>().isKinematic = false;
	}

	void Update() {

		// Jumping behaviour
		Debug.Log(currJumpSpeed);
		if (jstatus != JumpStatus.Grounded) {
			if (jstatus == JumpStatus.GoingUp) {
				if (!paused) {
					currTime += Time.deltaTime;
					currJumpSpeed = 35f;
					character.transform.Translate(Vector3.up * currJumpSpeed * Time.deltaTime);
				}
			}
			else {
				if (!paused){
					currTime += Time.deltaTime;
					currJumpSpeed = -20f;
					character.transform.Translate(Vector3.up * currJumpSpeed * Time.deltaTime);
				}
			}
		}
		if (currTime >= jumpTime / 2 && currTime < jumpTime && jstatus != JumpStatus.GoingDown) {
			currTime = jumpTime / 2;
			jstatus = JumpStatus.GoingDown;
		}
		if (currTime >= jumpTime) {
			currTime = 0.0f;
			jstatus = JumpStatus.Grounded;
			currJumpSpeed = 0.0f;
		}

		// Moving Behaviour
		if (mstatus != MoveStatus.Grounded){
			character.transform.Translate(Vector3.forward * currDirectionalSpeed * Time.deltaTime);
		}

	}
}
