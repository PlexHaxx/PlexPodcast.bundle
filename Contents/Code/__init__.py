ART = 'art-default.jpg'
ICON = 'icon-default.png'
FEED_URL = 'http://plexapp.com/podcasts/podcast.xml'

####################################################################################################
def Start():

	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = 'Plex Podcast'
	TrackObject.thumb = R(ICON)

####################################################################################################     
@handler('/music/plexpodcast', 'Plex Podcast', thumb=ICON, art=ART)
def MainMenu():

	oc = ObjectContainer()
	feed = RSS.FeedFromURL(FEED_URL)

	for item in feed.entries:
		url = item.enclosures[0]['url']
		title = item.title
		summary = item.summary
		originally_available_at = Datetime.ParseDate(item.updated)
		duration = Datetime.MillisecondsFromString(item.itunes_duration)

		oc.add(CreateTrackObject(url=url, title=title, summary=summary, originally_available_at=originally_available_at, duration=duration))

	return oc

####################################################################################################
def CreateTrackObject(url, title, summary, originally_available_at, duration, include_container=False):

	if url.endswith('.mp3'):
		container = 'mp3'
		audio_codec = AudioCodec.MP3
	else:
		container = Container.MP4
		audio_codec = AudioCodec.AAC

	track_object = TrackObject(
		key = Callback(CreateTrackObject, url=url, title=title, summary=summary, originally_available_at=originally_available_at, duration=duration, include_container=True),
		rating_key = url,
		title = title,
		summary = summary,
		originally_available_at = originally_available_at,
		duration = duration,
		items = [
			MediaObject(
				parts = [
					PartObject(key=url)
				],
				container = container,
				audio_codec = audio_codec,
				audio_channels = 2
			)
		]
	)

	if include_container:
		return ObjectContainer(objects=[track_object])
	else:
		return track_object
