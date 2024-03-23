from models import Submission

relevant_submissions = [
Submission(id="1", url="https://aiti.no", created_utc=00000, title="I need a simple front end to fetch my headless CMS data. Maybe nocode? ", 
           selftext="""
           Before anyone says, “everyone has an idea for an app, keep dreaming”……
            This pitch for a successful application is not something I just came up with. it’s basically an evolution of my previous business which I closed down due to my mothers untimely death. My mental state impacted my ability to function and work, I still pay the bill for the 1-800 number that I still own and I also retain the patent and renew it when needed. At one point this 1-800 number business was bringing in about $200,000 a month gross earnings. it was a nationwide, phone number and service number.
            This was all about 10 years ago. I’m currently a successful business owner in Long Island and own about 10 laundromats. I’m looking into reviving this old profession, as I can see a vision of it, being way more useful now than it was before given the technology.
            I don’t want to dilute into much of what the application would be about. I only own the patent for the phone number and the service, but I do not own the idea of it being an application at this time.
            Before I go through with getting a patent on my name with my idea, I just want to know is it hard to get an application off the ground and be successful? I’m willing to invest about $800,000-$1 million into the company. But I know I probably will not be able to do it on my own and be as successful as Uber or something like that.
            I am located in New York, not far from Long Island. I do have a bachelors degree in business and entrepreneurship. Does anyone have recommendations for services in nyc that help build a start up? I don’t want to attempt this and waste money working with the wrong people.
            All advice is appreciated!
            """),
Submission(id="2", url="https://aiti.no", created_utc=00000, title="I have an interesting for an App, but I have no coding experience. Looking for someone with coding experience.",
           selftext="""
           Hi everyone! I have an idea for an app that I think could generate a lot of traction, however, I have no coding or computer science background.
           I am a law student (close to graduating) and have realized that it makes more sense to bring someone in who could take care of the coding end, rather than attempting to learn code myself while balancing my legal career.
           Where can I find someone who would be interested in joining this with me? Also, does anyone here have experience with having AI write code for them? Any advice would be greatly appreciated
            """),


]

irrelevant_submissions = [
    Submission(id="100", url="https://aiti.no", created_utc=00000, title="I need a simple front end to fetch my headless CMS data. Maybe nocode? ", 
                selftext="""
                Need to build LittleCode/NoCode supply chain NFC Tag website. Low cost. headless cms
                Hi. Via storyblok.com (or another headless cms or something? i was also thinking about using wordpress but idk) information about a product (text + images/videos) will be stored.
                I need to put the content somehow into a very simple website. The link of the website will be stored into a NFC tag.
                there are thousands of ways to do that. What’s the best/easiest way? Actually a wordpress website would be the best way i guess. but i dont really like wordpress that much, it is really slow…
                any other CMS you can recommend? or with a head
                do you know a cheaper alternative to storybloks? and a way to publish the content easy into a website?
                actually i’m a react dev but i didnt code for 2 years now and i need to get this done
                maybe i use a react boilerplate website where i fetch the headless CMS content?
                or maybe there is a SaaS for my “problem”?
                video i would host on bunnycdn (cheapest option) or for free on yt
                """)
]