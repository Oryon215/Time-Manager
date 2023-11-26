using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TimeManagementSource
{
    class NotEnoughTime: Exception
    {
        private List<Event> not_enough_time;
        public NotEnoughTime(List<Event> lst)
        {
            not_enough_time = lst;
        }

        public List<Event> ListEvents
        {
            get { return not_enough_time; }
            set { not_enough_time = value; }
        }
    }
}
