import React from "react"
import "./coordinatorComponentsStyle/inviteButton.scss"

function InviteButton({ open, ...props }) {
	return (
		<div className={"invite_button_container"}>
			<button onClick={open} className="btn_reset invite_button_mobile">
				Пригласить игрока
			</button>
		</div>
	)
}

export default InviteButton
