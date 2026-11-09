"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

# ------------------------------------------------------------
# CRITERION 1: TEN HUMAN-WRITTEN SAMPLES
# ------------------------------------------------------------

HUMAN_SAMPLES = [
    """Harlem has been one of the most important centers of Black cultural and political life in the country for a really long time, so this one means gentrification here more than just any other normal neighborhood change, because it affects a place with such a deep historical meaning.

When I was doing research, I also mentioned some research papers that showed Harlem's Black population was about 98% in 1950, but by 2010 it had fallen to just about 63%.. A key turning point for this was the 2008 rezoning of 125th Street. The city framed it as a revitalization, but the rezoning also made Harlem more attractive to investors and large-scale development. As more investment came in, the rents and property values kept rising, and this led to more pressure on the long-term residents, who were already vulnerable to being pushed out.""",

    """The final artwork in the exhibit, Kara Walker’s Fons Americanus, is an awe-inspiring sculpture placed in the center of the room. Fons Americanus is a towering fountain that references the Victoria Memorial in front of Buckingham Palace but reimagines it through the lens of the African diaspora and the transatlantic slave trade. The sculpture stands at approximately 13 meters high, crafted from a mixture of steel, wood, and a proprietary composite material. The fountain’s flowing water creates a relaxing ambience, symbolizing cleansing. Around its base are intricate carvings and figures that depict moments of pain and hardship that are transformed into resilience.""",

    """Opposite Ringgold’s mural, Jean-Michel Basquiat’s Untitled, is displayed on an exposed brick wall. The painting is spotlighted at low angles, casting shadows that accentuate the textures and layers. It is a representation of a skull composed of acrylic, spray paint, and oil stick on canvas. The skull is depicted with an x-ray-like vision that exposes the details of the painting. Expressive brushstrokes and contrasting colors bring the skull to life, showing hollow eye sockets, jagged teeth, and a raw, layered jawline. The exaggerated eyes and snarling mouth create a confrontational expression, and the pink tones create a sense of fragility.""",

    """In both the Nidanakatha and the Lotus Sutra, hagiography is used as more than just a way to glorify the story of the Buddha’s life. These stories elevate the Buddha into a cosmic healer, whose life and teachings are the cure for human suffering. In either the divine planning of the Buddha’s birth or the compassionate use of skillful means, the Buddha is portrayed as completely intentional and universally relevant. This is especially true in the Mahayana tradition, where the idea of a universal path to enlightenment is illustrated by the hagiographic model. Rather than the focus being on historical accuracy, these narratives create the Buddha’s life as a timeless myth, one that can adapt itself as it needs to for different audiences.""",

    """One concept from the reading that caught my attention was the discussion on throughput vs response time in chapter 1.6 on performance. After reading the chapter, I understood response time as the time it takes to complete one task, while throughput measures how much total work a system can accomplish during a given period of time. Thus, there isn’t always a single way to make a computer faster. This concept is important because understanding the distinction between these 2 metrics can be advantageous depending on the system and the goal in mind. For instance, a laptop which is meant for only a single user may prioritize getting your task done quickly. On the other hand, a large datacenter will care more about how many total tasks they can complete over time.""",

    """My understanding was only reinforced after reading this chapter: developers and system designers may have different goals when it comes to optimization. In the context of a web app, let’s say a user clicks on a button; the response time is how quickly the page takes to load new content or submit a form. Techniques can be used to reduce delay like caching. However, upgrading server resources or adding more scalability to databases could increase throughput to allow more users on the site at once. I think this example can be used as a way to understand how the same performance principles in the context of computer systems can be applied broadly across so many different fields of computer science.""",

    """Targeted improvements could better align the park with how it’s used. A public restroom near the entrance to the promenade would serve both movement and gathering areas, allowing visitors to stay longer and improving accessibility for families and older visitors. In addition, the entrance to the bridge along the promenade could be formalized as a small gathering node. Since people already cluster here, adding structured seating or a widened overlook would support existing use while improving comfort. NYC parks already host poetry events here; making these regular but low-intensity would align with the promenade’s existing atmosphere. These improvements reflect Garvin’s idea that public realms should offer something for everybody by supporting movement, rest, and cultural use within the same space.""",

    """The story of Pygmalion addresses the unglamorous side of marriage, but in a different way than the myths of Hephaestus. In Hephaestus’s story, the problem is that marriage is imperfect and unequal: he is mocked, his wife is unfaithful, and the gods treat it like comedy. In Ovid’s Pygmalion, the problem is the anxiety that love requires giving up control, since Pygmalion turns away from real women and falls in love with a statue that has no desire of its own. Both stories suggest that marriage and desire are tied up with power and the fear of being vulnerable, but Pygmalion’s story ends happily, with a marriage and a child, while Hephaestus’s is left humiliating and unresolved.""",

    """The parable of the physician in Chapter 16 offers a very explicit illustration of this hagiography. In fact, this one is particularly profound, as it highlights the Buddha as not just a healer but as the embodiment of divine medicine itself. In this story, a loving father returns home to find his children suffering after having “mistakenly drank poison” and begging him to “please cure us and save our lives.” (The Lotus Sutra, p. 280) Here, the poison represents delusion and spiritual naivety, conditions that prevent one from being able to perceive the truth, similar to how the children lose their senses.""",

    """These stories often involve supernatural events, divine planning, or even just exaggerated qualities to portray the person as more than human. The main goal of hagiography in Buddhism is to both elevate the Buddha as a miracle worker and mythologize his life to present him as a spiritual and cosmic physician. This becomes even more true in the context of Mahayana texts, as the path to enlightenment is expanded to every being through the concept of “One Vehicle.” In a way, this model of hagiography prioritizes function over fact in order to become a tool to justify new teachings as divine medicine and promote universal salvation."""
]

# ------------------------------------------------------------
# CRITERION 2: TEN AI-GENERATED SAMPLES
# ------------------------------------------------------------

# These are newly generated evaluation samples, not the
# previously used calibration samples.
# Keep these exact texts unchanged across all three trials.

AI_SAMPLES = [
    """Public libraries are often described as places where people borrow books, but their role in a community is much broader. A library can provide reliable internet access, quiet study space, help with job applications, and programs for children and older adults. These services matter because not everyone has the same resources at home. A student who shares a crowded apartment may need a quiet place to complete assignments, while someone looking for work may need a computer to prepare a résumé. Libraries also create opportunities for people to encounter ideas and perspectives beyond their immediate surroundings. Their value therefore cannot be measured only by circulation numbers. A well-supported library strengthens a neighborhood by making information, technology, and public space available to people regardless of income.""",

    """Urban parks contribute to public health in ways that extend beyond exercise. Trees provide shade, vegetation can reduce the heat experienced by nearby residents, and open spaces give people opportunities to spend time outdoors. Parks also serve as shared environments where neighbors who might not otherwise meet can interact. However, these benefits are not distributed equally. Some neighborhoods have large, well-maintained parks, while others have limited green space or facilities that are difficult to access. Planning decisions should therefore consider both the amount of parkland and its location, condition, and accessibility. Community input is important because residents understand how public spaces are actually used. Investing in parks can improve daily life, but those investments are most effective when they respond to local needs and remain affordable for the people who live nearby.""",

    """Online education has made it easier for students to access courses without traveling to a physical campus. Recorded lectures allow learners to review difficult material, and discussion platforms can connect students who have different schedules. At the same time, flexibility does not automatically produce a better learning experience. Students may struggle to stay motivated when they have little direct contact with instructors or classmates. Technical problems and limited access to a quiet study environment can create additional barriers. A successful online course therefore needs more than uploaded videos. It should include clear weekly expectations, timely feedback, opportunities to ask questions, and activities that encourage participation. When these elements are thoughtfully designed, online learning can expand educational access while still giving students the structure and support needed to make progress.""",

    """A city transportation system should be evaluated by more than the speed of individual vehicles. Reliability, affordability, safety, and accessibility all influence whether people can reach work, school, medical appointments, and other important destinations. A route that is fast during ideal conditions may still be inconvenient if service is infrequent or unpredictable. Similarly, a station may be nearby but unusable for someone who cannot navigate stairs. Transportation planning should examine the entire journey, including walking connections, transfers, and the cost of fares. Public feedback can reveal problems that are not obvious from route maps or average travel times. By considering different passengers and their daily routines, planners can design systems that are not only efficient but also more equitable and dependable.""",

    """Small businesses often depend on relationships with customers in addition to the products or services they provide. A neighborhood shop may remember regular visitors, respond quickly to local preferences, and contribute to the character of a commercial street. These advantages can help a business compete with larger companies, but they do not remove financial pressures. Rent, staffing, inventory, and changing customer habits can make it difficult to remain profitable. Digital tools may help owners reach new customers or manage orders, although adopting new technology also requires time and money. Support for small businesses should therefore consider practical needs such as affordable commercial space, accessible financing, and useful training. Their long-term success benefits both business owners and the communities that rely on nearby services and employment.""",

    """In a well-designed software application, the interface should help users understand what is happening and what they can do next. Clear labels, predictable navigation, and useful error messages reduce the effort required to complete a task. These details may appear minor, but they influence whether people trust the application. For example, a form that reports only that something went wrong leaves users uncertain about how to recover. A better message identifies the problem and explains how to correct it. Designers should also consider people using different devices, assistive technologies, and levels of technical experience. Usability testing can reveal confusing interactions before a product is released. The goal is not simply to make an interface attractive; it is to make common tasks understandable, efficient, and accessible.""",

    """Museums preserve objects from the past, but their work also involves deciding how those objects should be interpreted and presented. An exhibition can influence visitors through the items it includes, the order in which they appear, and the explanations placed beside them. Because collections often reflect unequal histories of ownership and power, museums must consider whose experiences are represented and whose perspectives may be missing. Collaboration with source communities can lead to more responsible descriptions and decisions about display. This process does not mean that every historical disagreement can be resolved easily. It does mean that curators should explain the evidence behind their interpretations and remain open to revision. Museums become more meaningful public institutions when they treat visitors as people capable of asking questions rather than simply receiving information.""",

    """Household energy use is shaped by both individual choices and the design of buildings and infrastructure. Turning off unused lights can reduce consumption, but heating and cooling systems often account for a much larger share of energy demand. Insulation, efficient appliances, and well-sealed windows can lower the amount of energy needed to maintain comfortable indoor temperatures. However, upgrades may be expensive, especially for renters who do not control building improvements. Programs that provide financial assistance can help make efficiency measures available to more households. Energy policy should also consider the reliability and environmental effects of the electricity supply itself. Reducing consumption is useful, but lasting progress requires coordinated decisions by residents, property owners, utilities, and governments.""",

    """Team projects can help students develop skills that are difficult to practice through individual assignments alone. Members must divide responsibilities, communicate progress, and make decisions when their ideas differ. These interactions can reveal strengths that are not always visible in written assessments, such as explaining a technical concept or helping a group recover from a missed deadline. However, group work can become frustrating when expectations are unclear or when a few people complete most of the tasks. Teams benefit from agreeing on roles, deadlines, and methods for sharing updates at the beginning of a project. Regular check-ins make it easier to identify problems before they become serious. A successful collaboration does not require everyone to contribute in exactly the same way, but each member should have a meaningful responsibility.""",

    """Public art changes how people experience shared spaces by introducing images, structures, and ideas into everyday surroundings. A mural on a blank wall can make a street more visually distinctive, while a sculpture in a plaza may encourage visitors to pause and gather. The meaning of an artwork is not determined only by the artist. Residents may connect it to local history, disagree with its message, or question why a particular subject was selected. For that reason, public art projects benefit from transparent planning and opportunities for community participation. Practical concerns also matter, including maintenance, accessibility, and the possibility that redevelopment could displace existing residents. Public art can strengthen a sense of place, but it works best when it reflects an ongoing relationship with the community rather than serving only as decoration."""
]



SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": HUMAN_SAMPLES,
    },
    {
        "name": "ai generated writing",
        "criterion": 2,
        "texts": AI_SAMPLES,
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # Reuse the same fixed human and AI samples.
        # This checks whether all three labels are reachable.
        "texts": HUMAN_SAMPLES + AI_SAMPLES,
    },
    {
        "name": "invalid submissions",
        "criterion": 5,
        "bodies": [
            # Empty text
            {"text": "", "creator_id": "eval_bad_empty"},

            # Missing text field
            {"creator_id": "eval_bad_missing_text"},

            # Null text
            {"text": None, "creator_id": "eval_bad_null_text"},

            # Non-string text
            {"text": 12345, "creator_id": "eval_bad_numeric_text"},

            # Whitespace-only text
            {"text": "   ", "creator_id": "eval_bad_whitespace_text"},

            # Missing creator_id
            {"text": "This is a valid length submission.",},

            # Empty creator_id
            {"text": "This is a valid length submission.", "creator_id": ""},

            # Whitespace-only creator_id
            {"text": "This is a valid length submission.", "creator_id": "   "},

            # Null creator_id
            {"text": "This is a valid length submission.", "creator_id": None},

            # Non-string creator_id
            {"text": "This is a valid length submission.", "creator_id": 12345},

            # Fewer than three GPT-2 tokens
            {"text": "Hi", "creator_id": "eval_bad_short"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
