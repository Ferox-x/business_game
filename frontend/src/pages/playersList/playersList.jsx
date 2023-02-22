import React from "react"
import "./playersList.scss"
import PlayersTable from "./modules/playersTable"
import Layout from "../../components/layouts/layout"

function PlayersList(props) {
	return (
		<Layout>
			<div className="player_list_body">
				<PlayersTable />
			</div>
		</Layout>
	)
}

export default PlayersList
