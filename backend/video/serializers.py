"""video serializers"""

# pylint: disable=abstract-method

from channel.serializers import ChannelSerializer
from common.serializers import PaginationSerializer
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from video.src.constants import OrderEnum, SortEnum, VideoTypeEnum, WatchedEnum


class PlayerSerializer(serializers.Serializer):
    """serialize player"""

    watched = serializers.BooleanField()
    watched_date = serializers.IntegerField(required=False)
    duration = serializers.IntegerField()
    duration_str = serializers.CharField()

    progress = serializers.FloatField(required=False)
    position = serializers.FloatField(required=False)


class SponsorBlockSegmentSerializer(serializers.Serializer):
    """serialize sponsorblock segment"""

    actionType = serializers.CharField()
    videoDuration = serializers.FloatField()
    segment = serializers.ListField(child=serializers.FloatField())
    votes = serializers.IntegerField()
    category = serializers.CharField()
    UUID = serializers.CharField()
    locked = serializers.IntegerField()


class SponsorBlockSerializer(serializers.Serializer):
    """serialize sponsorblock"""

    is_enabled = serializers.BooleanField()
    last_refresh = serializers.IntegerField()
    has_unlocked = serializers.BooleanField(required=False)
    segments = SponsorBlockSegmentSerializer(many=True)


class LostMediaFinderLinkContainsSerializer(serializers.Serializer):
    """serialize lostmediafinder link contains"""

    video = serializers.BooleanField()
    metadata = serializers.BooleanField()
    comments = serializers.BooleanField()
    thumbnail = serializers.BooleanField()
    captions = serializers.BooleanField()
    standalone_video = serializers.BooleanField()
    standalone_audio = serializers.BooleanField()
    single_frame = serializers.BooleanField()


class LostMediaFinderLinkSerializer(serializers.Serializer):
    """serialize lostmediafinder link"""

    _type = serializers.CharField()
    classname = serializers.CharField()
    type = serializers.CharField()
    url = serializers.URLField()
    title = serializers.CharField()
    note = serializers.CharField(required=False)
    contains = LostMediaFinderLinkContainsSerializer()


class LostMediaFinderServiceSerializer(serializers.Serializer):
    """serialize lostmediafinder service"""

    _type = serializers.CharField()
    classname = serializers.CharField()
    type = serializers.CharField()
    name = serializers.CharField()
    lastupdated = serializers.IntegerField()
    archived = serializers.BooleanField()
    metaonly = serializers.BooleanField()
    comments = serializers.BooleanField()
    maybe_paywalled = serializers.BooleanField()
    note = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
    available = LostMediaFinderLinkSerializer(many=True)
    # This field is not used as of 2025-10-01
    # suppl = serializers.CharField(required=False)
    # This field is just a dump of the original data
    # rawraw = serializers.CharField(required=False)


class LostMediaFinderVerdictSerializer(serializers.Serializer):
    """serialize lostmediafinder verdict"""

    video = serializers.BooleanField()
    metaonly = serializers.BooleanField()
    comments = serializers.BooleanField()
    human_friendly = serializers.CharField()


class LostMediaFinderSearchResultSerializer(serializers.Serializer):
    """serialize lostmediafinder search_result"""

    _type = serializers.CharField()
    api_version = serializers.IntegerField()
    id = serializers.CharField()
    status = serializers.CharField()
    verdict = LostMediaFinderVerdictSerializer()
    keys = LostMediaFinderServiceSerializer(many=True)


class LostMediaFinderSerializer(serializers.Serializer):
    """serialize lostmediafinder"""

    last_refresh = serializers.IntegerField()
    verdict = LostMediaFinderVerdictSerializer()
    search_result = LostMediaFinderSearchResultSerializer()


class StatsSerializer(serializers.Serializer):
    """serialize stats"""

    like_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    view_count = serializers.IntegerField()
    dislike_count = serializers.IntegerField()


class StreamItemSerializer(serializers.Serializer):
    """serialize stream item"""

    bitrate = serializers.IntegerField()
    codec = serializers.CharField()
    height = serializers.IntegerField(required=False)
    index = serializers.IntegerField()
    type = serializers.ChoiceField(choices=["video", "audio"])
    width = serializers.IntegerField(required=False)


class SubtitleFragmentSerializer(serializers.Serializer):
    """serialize subtitle fragment"""

    subtitle_channel = serializers.CharField()
    subtitle_channel_id = serializers.CharField()
    subtitle_end = serializers.CharField()
    subtitle_fragment_id = serializers.CharField()
    subtitle_index = serializers.IntegerField()
    subtitle_lang = serializers.CharField()
    subtitle_last_refresh = serializers.IntegerField()
    subtitle_line = serializers.CharField()
    subtitle_source = serializers.ChoiceField(choices=["user", "auto"])
    subtitle_start = serializers.CharField()
    title = serializers.CharField()
    youtube_id = serializers.CharField()


class SubtitleItemSerializer(serializers.Serializer):
    """serialize subtitle item"""

    ext = serializers.ChoiceField(choices=["json3", "vtt"])
    lang = serializers.CharField()
    media_url = serializers.CharField()
    name = serializers.CharField()
    source = serializers.ChoiceField(choices=["user", "auto"])
    url = serializers.URLField(allow_null=True)


class VideoSerializer(serializers.Serializer):
    """serialize video item"""

    active = serializers.BooleanField()
    category = serializers.ListField(child=serializers.CharField())
    channel = ChannelSerializer(required=False)
    comment_count = serializers.IntegerField(allow_null=True, required=False)
    date_downloaded = serializers.IntegerField()
    description = serializers.CharField(allow_null=True, required=False)
    media_size = serializers.IntegerField()
    media_url = serializers.CharField()
    player = PlayerSerializer()
    playlist = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    published = serializers.CharField()
    sponsorblock = SponsorBlockSerializer(allow_null=True, required=False)
    lostmediafinder = LostMediaFinderSerializer(allow_null=True)
    stats = StatsSerializer()
    streams = StreamItemSerializer(many=True)
    subtitles = SubtitleItemSerializer(many=True, required=False)
    tags = serializers.ListField(child=serializers.CharField())
    title = serializers.CharField()
    vid_last_refresh = serializers.CharField()
    vid_thumb_url = serializers.CharField()
    vid_type = serializers.ChoiceField(choices=VideoTypeEnum.values_known())
    youtube_id = serializers.CharField()
    _index = serializers.CharField(required=False)
    _score = serializers.FloatField(required=False)


class VideoListSerializer(serializers.Serializer):
    """serialize video list"""

    data = VideoSerializer(many=True)
    paginate = PaginationSerializer()


class VideoListQuerySerializer(serializers.Serializer):
    """serialize query for video list"""

    playlist = serializers.CharField(required=False)
    channel = serializers.CharField(required=False)
    watch = serializers.ChoiceField(
        choices=WatchedEnum.values(), required=False, allow_null=True
    )
    sort = serializers.ChoiceField(choices=SortEnum.names(), required=False)
    order = serializers.ChoiceField(choices=OrderEnum.values(), required=False)
    type = serializers.ChoiceField(
        choices=VideoTypeEnum.values_known(), required=False
    )
    page = serializers.IntegerField(required=False)
    height = serializers.IntegerField(required=False)


class CommentItemSerializer(serializers.Serializer):
    """serialize comment item"""

    comment_author = serializers.CharField()
    comment_author_id = serializers.CharField()
    comment_author_is_uploader = serializers.BooleanField()
    comment_author_thumbnail = serializers.URLField()
    comment_id = serializers.CharField()
    comment_is_favorited = serializers.BooleanField()
    comment_likecount = serializers.IntegerField()
    comment_parent = serializers.CharField()
    comment_text = serializers.CharField()
    comment_time_text = serializers.CharField()
    comment_timestamp = serializers.IntegerField()

    comment_replies = serializers.SerializerMethodField()

    @extend_schema_field(serializers.ListField())
    def get_comment_replies(self, obj):
        """recursive replies"""
        return CommentItemSerializer(
            obj.get("comment_replies", []), many=True
        ).data


class CommentsSerializer(serializers.Serializer):
    """serialize comments as indexed"""

    comment_channel_id = serializers.CharField()
    comment_comments = CommentItemSerializer(many=True)
    comment_last_refresh = serializers.IntegerField()
    youtube_id = serializers.CharField()


class PlaylistNavMetaSerializer(serializers.Serializer):
    """serialize playlist nav meta"""

    current_idx = serializers.IntegerField()
    playlist_id = serializers.CharField()
    playlist_name = serializers.CharField()
    playlist_channel = serializers.CharField()


class PlaylistNavVideoSerializer(serializers.Serializer):
    """serialize video item on playlist nav"""

    youtube_id = serializers.CharField()
    title = serializers.CharField()
    uploader = serializers.CharField()
    idx = serializers.IntegerField()
    downloaded = serializers.BooleanField()
    vid_thumb = serializers.CharField()


class PlaylistNavItemSerializer(serializers.Serializer):
    """serialize nav on playlist"""

    playlist_meta = PlaylistNavMetaSerializer()
    playlist_previous = PlaylistNavVideoSerializer(allow_null=True)
    playlist_next = PlaylistNavVideoSerializer(allow_null=True)


class VideoProgressUpdateSerializer(serializers.Serializer):
    """serialize progress update data"""

    position = serializers.FloatField(default=0)
