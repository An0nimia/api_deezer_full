def get_media_right() -> str:
	return (
		'''
			rights {
				ads {
					available
					availableAfter
				}

				sub {
					available
					availableAfter
				}

				upload {
					available
				}
			}
		'''
	)

def get_media() -> str:
	return (
		f'''
			id
			version
			token {{
				payload
				expiresAt
			}}
			estimatedSizes {{
				SBC_256
				AAC_64
				AAC_96
				MP3_MISC
				MP3_32
				MP3_64
				MP3_128
				MP3_192
				MP3_256
				MP3_320
				FLAC
				MP4_RA1
				MP4_RA2
				MP4_RA3
				DD_JOC
				AC4_IMS
			}}
		'''
	)


def get_album_fallback() -> str:
	return (
		f'''
			id
			displayTitle
			cover {{
				url: urls(pictureRequest: {{width: 1400, height: 1400}})
			}}
			label
			producerLine
			copyright
			duration
			
			releaseDate
			fansCount
			isExplicit
			isTakenDown
			discsCount
			tracksCount
		'''
	)


def get_track() -> str:
	return (
		f'''
			id
			title
			ISRC
			{get_disk_info()}
			duration
			gain
			bpm
			popularity
			releaseDate
			album {{
				{
					get_album_x_track()
				}
			}}
			{get_contributors_edges()}
			isExplicit
			lyrics {{
				{
					get_lyric()
				}
			}}
			media {{
				{
					get_media()
				}
			}}
			isFavorite
			isBannedFromRecommendation
		'''
	)


def get_track_edges() -> str:
	return (
		f'''
			edges {{
				node {{
					{
						get_track()
					}
				}}
			}}
		'''
	)


def get_track_x_album() -> str:
	return (
		f'''
			edges {{
				node {{
					id
					title
					ISRC
					{get_disk_info()}
					duration
					gain
					bpm
					popularity
					releaseDate
					{get_contributors_edges()}
					isExplicit
					lyrics {{
						{
							get_lyric()
						}
					}}
					media {{
						{
							get_media()
						}
					}}
					isFavorite
					isBannedFromRecommendation
				}}
			}}
		'''
	)


def get_album_x_track() -> str:
	return (
		f'''
			id
			displayTitle
			cover {{
				url: urls(pictureRequest: {{width: 1400, height: 1400}})
			}}
			label
			producerLine
			copyright
			duration
			{get_contributors_edges()}
			releaseDate
			fansCount
			isExplicit
			isTakenDown
			fallback {{
				{
					get_album_fallback()
				}
			}}
			discsCount
			tracksCount
		'''
	)


def get_album() -> str:
	return (
		f'''
			id
			displayTitle
			cover {{
				url: urls(pictureRequest: {{width: 1400, height: 1400}})
			}}
			label
			producerLine
			copyright
			duration
			{get_contributors_edges()}
			releaseDate
			fansCount
			isExplicit
			isTakenDown
			tracks(first: 50) {{
				{
					get_track_x_album()
				}
			}}
			fallback {{
				{
					get_album_fallback()
				}
			}}
			discsCount
			tracksCount
		'''
	)


def get_lyric() -> str:
	return (
		'''
			id
			synchronizedLines {
				lrcTimestamp
				line
				milliseconds
				duration
			}
			text
			copyright
			writers
		'''
	)


def get_disk_info() -> str:
	return (
		'''
			diskInfo {
				diskNumber
				trackNumber
			}
		'''
	)


def get_artist() -> str:
	return (
		'''
			id
			name
			fansCount
			onTour
			status
			picture {
				url: urls(pictureRequest: {width: 1400, height: 1400})
			}
		'''
	)


def get_contributors_edges() -> str:
	return (
		f'''
			contributors(first: 18) {{
				edges {{
					roles
					node {{
						... on Artist {{
							{
								get_artist()
							}
						}}	
					}}
				}}
			}}
		'''
	)


def get_playlist() -> str:
	return (
		f'''
			id
			title
			description
			isPrivate
			isCollaborative
			isCharts
			isBlindTestable
			isFromFavoriteTracks
			isEditorialized
			linkedArtist {{
				{
					get_artist()
				}
			}}
			picture {{
				url: urls(pictureRequest: {{width: 1400, height: 1400}})
			}}
			estimatedTracksCount
			estimatedDuration
			creationDate
			lastModificationDate
			fansCount
			isFavorite
			tracks(first: 25) {{
				{
					get_track_edges()
				}
			}}
		'''
	)


def get_introspection() -> str:
	return (
		'''
			query IntrospectionQuery {
			__schema {
				
				queryType { name }
				mutationType { name }
				subscriptionType { name }
				types {
				...FullType
				}
				directives {
				name
				description
				
				locations
				args {
					...InputValue
				}
				}
			}
			}

			fragment FullType on __Type {
			kind
			name
			description
			
			fields(includeDeprecated: true) {
				name
				description
				args {
				...InputValue
				}
				type {
				...TypeRef
				}
				isDeprecated
				deprecationReason
			}
			inputFields {
				...InputValue
			}
			interfaces {
				...TypeRef
			}
			enumValues(includeDeprecated: true) {
				name
				description
				isDeprecated
				deprecationReason
			}
			possibleTypes {
				...TypeRef
			}
			}

			fragment InputValue on __InputValue {
			name
			description
			type { ...TypeRef }
			defaultValue
			
			
			}

			fragment TypeRef on __Type {
			kind
			name
			ofType {
				kind
				name
				ofType {
				kind
				name
				ofType {
					kind
					name
					ofType {
					kind
					name
					ofType {
						kind
						name
						ofType {
						kind
						name
						ofType {
							kind
							name
						}
						}
					}
					}
				}
				}
			}
			}
		'''
	)