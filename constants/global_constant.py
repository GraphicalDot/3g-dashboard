# //////////////////////////////////////////////////////////////
# ////////////////////////// CONSTANTS /////////////////////////
# //////////////////////////////////////////////////////////////


from classes.models import (BoardCategory, ClassCategory)
from course_management.models import (Course, Topic, Subject, Chapter, ModuleData)
from collections import OrderedDict
from country_state.models import State

PERMISSION_NAME_FORMAT = ['crud', 'BoardCategory', 'ClassCategory', 'Course',
                          'Subject', 'Chapter', 'Topic', 'ModuleData']

PERMISSION_CODENAME_FORMAT = {'boardcategory': BoardCategory, 'classcategory': ClassCategory,
                              'course': Course, 'subject': Subject, 'chapter': Chapter,
                              'topic': Topic, 'moduledata': ModuleData
                              }

FILTER_ON_DYNAMIC_MODELS = OrderedDict({'boardcategory': BoardCategory, 'classcategory': ClassCategory,
                              'course': Course, 'subject': Subject, 'chapter': Chapter,
                              'topic': Topic, 'moduledata': ModuleData
                              })

PARENT_KEY_CHILD_VALUE = {'country': State, 'state': BoardCategory, 'board': ClassCategory,
                          'grade': Course, 'stream': Subject, 'subject': Chapter}

GLOBAL_LIST_DISPLAY = ('get_title', 'is_live')

MULTI_SELECT_GRADE_HELP = "<b style='font-size:15px;'>Select above checkbox " \
                          "to choose from existing grade(s).</b>"

PRE_SELECT_GRADE_MSG = "<b style='color:black;'>Pre-Selected: " \
                       "</b><span style='background:yellow; color:red'>{0}</span>"
