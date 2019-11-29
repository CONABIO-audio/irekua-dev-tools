REPOSITORY_INFO = {
    'selia-visualizers': {
        'url': 'https://github.com/CONABIO-audio/selia-visualizers',
        'git': 'git@github.com:CONABIO-audio/selia-visualizers.git',
        'dependencies': [
            'irekua-dev-settings',
            'irekua-database',
        ],
    },
    'selia-uploader': {
        'url': 'https://github.com/CONABIO-audio/selia-uploader',
        'git': 'git@github.com:CONABIO-audio/selia-uploader.git',
        'dependencies': [
            'irekua-dev-settings',
            'irekua-database',
            'irekua-rest-api',
            'selia-templates',
            'selia-thumbnails',
        ],
    },
    'selia-thumbnails': {
        'url': 'https://github.com/CONABIO-audio/selia-thumbnails',
        'git': 'git@github.com:CONABIO-audio/selia-thumbnails.git',
        'dependencies': [
            'irekua-dev-settings',
            'irekua-database',
        ],
    },
    'selia-templates': {
        'url': 'https://github.com/CONABIO-audio/selia-templates',
        'git': 'git@github.com:CONABIO-audio/selia-templates.git',
        'dependencies': [
            'selia-forms',
        ],
    },
    'selia-registration': {
        'url': 'https://github.com/CONABIO-audio/selia-registration',
        'git': 'git@github.com:CONABIO-audio/selia-registration.git',
        'dependencies': [
            'irekua-dev-settings',
            'irekua-database',
            'selia-forms',
            'selia-templates',
        ],
    },
    'selia-forms': {
        'url': 'https://github.com/CONABIO-audio/selia-forms',
        'git': 'git@github.com:CONABIO-audio/selia-forms.git',
        'dependencies': [],
    },
    'selia-annotator': {
        'url': 'https://github.com/CONABIO-audio/selia-annotator',
        'git': 'git@github.com:CONABIO-audio/selia-annotator.git',
        'dependencies': [
            'irekua-dev-settings',
            'irekua-database',
            'irekua-rest-api',
            'selia-templates',
            'selia-visualizers'
        ],
    },
    'selia-admin': {
        'url': 'https://github.com/CONABIO-audio/selia-admin',
        'git': 'git@github.com:CONABIO-audio/selia-admin.git',
        'dependencies': [
            'irekua-dev-settings',
            'irekua-database',
            'selia-annotator',
            'selia-visualizers',
        ],
    },
    'selia-about': {
        'url': 'https://github.com/CONABIO-audio/selia-about',
        'git': 'git@github.com:CONABIO-audio/selia-about.git',
        'dependencies': [
            'irekua-dev-settings',
            'selia-templates'
        ],
    },
    'selia': {
        'url': 'https://github.com/CONABIO-audio/selia',
        'git': 'git@github.com:CONABIO-audio/selia.git',
        'dependencies': [
            'irekua-dev-settings',
            'irekua-database',
            'irekua-filters',
            'irekua-permissions',
            'irekua-rest-api',
            'irekua-autocomplete',
            'selia-forms',
            'selia-templates',
            'selia-registration',
            'selia-about',
            'selia-visualizers',
            'selia-annotator',
            'selia-thumbnails',
            'selia-uploader'
        ],
    },
    'irekua-rest-api': {
        'url': 'https://github.com/CONABIO-audio/irekua-rest-api',
        'git': 'git@github.com:CONABIO-audio/irekua-rest-api.git',
        'dependencies': [
            'irekua-dev-settings',
            'irekua-database'
        ],
    },
    'irekua-database': {
        'url': 'https://github.com/CONABIO-audio/irekua-database',
        'git': 'git@github.com:CONABIO-audio/irekua-database.git',
        'dependencies': [
            'irekua-dev-settings',
        ],
    },
    'irekua-autocomplete': {
        'url': 'https://github.com/CONABIO-audio/irekua-autocomplete',
        'git': 'git@github.com:CONABIO-audio/irekua-autocomplete.git',
        'dependencies': [
            'irekua-dev-settings',
            'irekua-database'
        ]
    },
    'irekua-permissions': {
        'url': 'https://github.com/CONABIO-audio/irekua-permissions',
        'git': 'git@github.com:CONABIO-audio/irekua-permissions.git',
        'dependencies': [
            'irekua-database',
        ]
    },
    'irekua-filters': {
        'url': 'https://github.com/CONABIO-audio/irekua-filters',
        'git': 'git@github.com:CONABIO-audio/irekua-filters.git',
        'dependencies': [
            'irekua-database',
        ],
    },
    'irekua-dev-settings': {
        'url': 'https://github.com/CONABIO-audio/irekua-dev-settings',
        'git': 'git@github.com:CONABIO-audio/irekua-dev-settings.git',
        'dependencies': [
        ],
    },
}
