import React from "react"
import Notification from "./notice"
import { useSelector } from "react-redux"
import "./style/notifications.scss"

function Notifications(props) {
	const notifications = useSelector((state) => state.notice)

	return (
		<div className="notifications_container">
			{notifications.map((notice) => {
				return (
					<Notification
						key={notice.id}
						id={notice.id}
						message={notice.message}
						status={notice.status}
					/>
				)
			})}
		</div>
	)
}

export default Notifications
