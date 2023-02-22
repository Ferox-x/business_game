import React from "react"
import { useDispatch } from "react-redux"
import { useEffect, useState } from "react"
import ProfileWithOutData from "./playerProfile/modules/profileWithOutData"
import ProfileWithData from "./playerProfile/modules/profileWithData"
import { PlayerInfo } from "./api/playerProfileApi"

function PlayerProfile(props) {
	const dispatch = useDispatch()

	function getData() {
		new PlayerInfo(dispatch).getData().then((response) => {
			if (response.status === 200) {
				setData(response.data)
			}
		})
	}

	useEffect(() => {
		new PlayerInfo(dispatch).getPlayerInfo()
		getData()
	}, [])

	const [data, setData] = useState(null)

	const without_data = <ProfileWithOutData />

	const with_data = <ProfileWithData data={data} />

	return <>{data ? with_data : without_data}</>
}

export default PlayerProfile
