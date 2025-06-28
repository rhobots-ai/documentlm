import mimetypes
from core.models import DataSource

def create_data_source(created_by, is_platform, title=None, url: str = None, file=None):
    """
    Creates a DataSource instance based on a URL or file.
    """
    if not created_by:
        raise ValueError("created_by is required")

    if not url and not file:
        raise ValueError("Either file or url must be provided")

    if url:
        title = title or url
        data_source = DataSource.objects.create(
            created_by=created_by,
            title=title,
            data_type='url',
            data={},
            is_created_via_platform=is_platform,
        )
        return data_source

    if file:
        mime_type, _ = mimetypes.guess_type(file.name)
        data_type = _infer_data_type_from_mime(mime_type)

        title = title or file.name
        data_source = DataSource.objects.create(
            created_by=created_by,
            title=title,
            data_type=data_type,
            file=file,
            size=file.size,
            data={},
            is_created_via_platform=is_platform,
        )
        return data_source

    raise ValueError("Invalid input")


def _infer_data_type_from_mime(mime_type):
    if mime_type is None:
        return 'document'  # fallback
    if mime_type.startswith('text'):
        return 'text'
    elif mime_type.startswith('audio'):
        return 'audio'
    elif mime_type.startswith('video'):
        return 'video'
    elif mime_type.startswith('image'):
        return 'image'
    elif mime_type in ['application/pdf', 'application/msword',
                       'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        return 'document'
    return 'document'  # default fallback
