import React from "react"
import "./styles/playersList.scss"
import Layout from "../../components/layouts/layout"
import PlayersListTable from "./modules/playersListTable"
import { useState } from "react"
import { PlayersListAPI } from "./api/playersListAPI"
import Pagination from "../../components/paginator/pagination"

function PlayersList(props) {
	const [data, setData] = useState([])

	function getPlayersPerPage(page) {
		return PlayersListAPI.getPlayersPerPage(page)
	}

	return (
		<>
			<Layout>
				<div className="players_list">
					<PlayersListTable value={data} />
					<Pagination callback={getPlayersPerPage} setValue={setData} />
				</div>
			</Layout>
		</>
	)
}

export default PlayersList
