ART = 'art-default.jpg'
ICON = 'icon-default.png'
FEED_URL = 'http://plexapp.com/podcasts/podcast.xml'

####################################################################################################
def Start():
    Plugin.AddPrefixHandler('/music/plexpodcast', MainMenu, 'Plex Podcast', ICON, ART)
    
    ObjectContainer.art = R(ART)
    ObjectContainer.title1 = 'Plex Podcast'
    
    TrackObject.thumb = R(ICON)
    
####################################################################################################     
def MainMenu():
    oc = ObjectContainer()
    
    feed = RSS.FeedFromURL(FEED_URL)
    
    for item in feed.entries:
        title = item.title
        summary = item.summary
        date = item.updated
        url = item.enclosures[0]['url']
        duration = Datetime.MillisecondsFromString(item.itunes_duration)
        oc.add(TrackObject(key=url, rating_key=url, title=title, summary=summary, originally_available_at=Datetime.ParseDate(date).date(), duration=duration,
                           items = [
            MediaObject(
                parts = [PartObject(key=url)],
                container = Container.MP4,
                audio_codec = AudioCodec.AAC,
                audio_channels = 2
            )
        ]))
    
    return oc
