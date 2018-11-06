using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;

public class HoldButton : MonoBehaviour, IPointerDownHandler, IPointerUpHandler {

	bool isPressed = false;
	public Movement mov;

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		
		if (this.gameObject.name == "Left")
			mov.MoveLeft(isPressed);
		else if (this.gameObject.name == "Right")
			mov.MoveRight(isPressed);
	}

	public void OnPointerDown(PointerEventData eventData){
		isPressed = true;
	}

	public void OnPointerUp(PointerEventData eventData){
		isPressed = false;
	}
}
