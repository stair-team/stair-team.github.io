---
# Leave the homepage title empty to use the site title
title:
date: 2022-10-24
type: landing
summary: STAIR Research Group at ICT, CAS researches scalable and trustworthy AI, spanning trustworthy foundation models and agents, high-quality graph data, and agentic reasoning.

sections:
  - block: hero
    design:
        css_class: "hero-large"
        spacing:
          padding: ["80px", "0px", "20px", "0px"]
    content:
      title: |
        <span style="font-size: 0.9em;">STAIR</span>
      image:
        filename: BGT-Mlogo.png
      text: |
        <div style="font-size: 1rem;">
        <br>
        We are focusing on <u>s</u>calable and <u>t</u>rustworthy <u>AI</u> <u>r</u>esearches, spanning AI for trustworthy foundation models and agents, reasoning and efficiency scaling, and scalable algorithms especially on big graphs, aiming at bridging large language models (LLMs) and graph intelligence to tackle real-world challenges. 
        The group is directed by Shenghua Liu at Institute of Computing Technology, Chinese Academy of Sciences (ICT, CAS). 
        Our goals include:
        <ul>
        <li> <strong>Trustworthy LLMs</strong>, building reliable, faithful, and capable foundation models and agents in the era of RSI, with an emphasis on AI-driven methods.
        <li> <strong>High-quality data</strong>, that is data mining methods related to big graph mining, scalable algorithms, graph compression, and summarization.
        <li> <strong>Agentic reasoning</strong>, agent reasoning over complex relational structures, and graph-structured organization of agent memory.
        </ul>
        <br>
        <br>
        <i> We are actively recruiting highly-motivated Researchers and Ph.D./M.S./visiting students to join our group at ICT, CAS! </i>
        </div>

  - block: people
    id: team
    content:
      title: Meet the Team
      subtitle: Our research group members
      # Choose which groups/teams of users to display.
      #   Edit `user_groups` in each user's profile to add them to one or more of these groups.
      user_groups:
          - Principal Investigator
          - Researchers
          - Students
          - Administration
          - Visitors
          - Postdocs
          - Alumni
          - Partners
      sort_by: Params.last_name
      sort_ascending: false
    design:
      show_interests: true
      show_role: true
      show_social: true
      spacing:
          padding: ["60px", "0px", "60px", "0px"]

---

# - block: about.biography

# id: about

# content:

# title: About

# # Choose a user profile to display (a folder name within `content/authors/`)

# username: admin

# design:

# spacing:

# padding: ["20px", "0", "20px", "0"]

# - block: collection

# id: Publications

# content:

# title: Publications

# text: |-

# {{% callout note %}}

# 🔍 Quickly discover relevant content by [filtering publications](./publication/).



# {{% /callout %}}



# filters:



# folders:



# - publication



# exclude_featured: false



# offset: 0



# order: desc



# design:



# spacing:



# padding: ["50px", "0px", "50px", "100px"]



# columns: '2'



# view: Citation



# - block: collection



# id: talks



# content:



# title: Recent & Upcoming Talks



# count: 5



# filters:



# folders:



# - event



# design:



# spacing:



# padding: ["50px", "0px", "50px", "100px"]



# columns: '2'



# view: compact



# - block: portfolio



# id: projects



# content:



# title: 开源项目



# filters:



# folders:



# - post



# # Default filter index (e.g. 0 corresponds to the first `filter_button` instance below).



# default_button_index: 0



# # Filter toolbar (optional).



# # Add or remove as many filters (`filter_button` instances) as you like.



# # To show all items, set `tag` to "*".



# # To filter by a specific tag, set `tag` to an existing tag name.



# # To remove the toolbar, delete the entire `filter_button` block.



# buttons:



# - name: All



# tag: '*'



# - name: 图方向



# tag: 'graph'



# - name: 大模型方向



# tag: 'LLMs'



# design:



# # Choose how many columns the section has. Valid values: '1' or '2'.



# columns: '1'



# view: showcase



# # For Showcase view, flip alternate rows?



# flip_alt_rows: false



# spacing:



# padding: ["50px", "0px", "20px", "0px"]



# - block: features



# content:



# title: 研究方向



# items:



# - name: 大图挖掘



# icon: python



# icon_pack: fab



# - name: 大语言模型



# icon: linux



# icon_pack: fab



# - name: 异常检测



# icon: overleaf



# icon_pack: ai



# - block: people



# id: peoples



# content:



# title: Meet the Team



# # Choose which groups/teams of users to display.



# #   Edit `user_groups` in each user's profile to add them to one or more of these groups.



# user_groups:



# - Principal Investigators



# - Researchers



# - Grad Students



# - Administration



# - Visitors



# - Alumni



# sort_by: Params.last_name



# sort_ascending: true



# design:



# show_interests: true



# show_role: true



# show_social: true



# spacing:



# padding: ["30px", "0px", "30px", "0px"]



# - block: accomplishments



# id: accomplishments



# content:



# # Note: `&shy;` is used to add a 'soft' hyphen in a long heading.



# title: '获奖'



# id: accomplishments



# # subtitle:



# # Date format: [https://docs.hugoblox.com/customization/#date-format](https://docs.hugoblox.com/customization/#date-format)



# date_format: Jan 2006



# items:



# - certificate_url:



# date_end: ''



# date_start: '2021-12-01'



# description: ''



# organization: THU



# organization_url:



# title: 进步奖



# #          url: ''



# - certificate_url:



# date_end: ''



# date_start: '2023-10-01'



# description: ''



# organization: THU



# organization_url:



# title: 'Best paper'



# url: ''



# - certificate_url:



# date_end: ''



# date_start: '2022-02-01'



# description: ''



# organization: microsoft



# organization_url: [https://openi.org.cn/](https://openi.org.cn/)



# title: 微软学者



# url: ''



# design:



# columns: '2'



# spacing:



# padding: ["50px", "0px", "50px", "0px"]



# - block: tag_cloud



# id: Topics



# content:



# title: 词云



# design:



# columns: '1'



# background:



# gradient_start: '#eef2f3'



# gradient_end: '#eef2f3'



# gradient_angle: 180



# text_color_light: false



# spacing:



# padding: ["30px", "0px", "30px", "0px"]



# - block: contact



# content:



# title: Contact



# text: |-



# 欢迎联系！



# email: [test@example.org](mailto:test@example.org)



# phone: 888 888 88 88



# address:



# street: 450 Serra Mall



# city: Stanford



# region: CA



# postcode: '94305'



# country: United States



# country_code: US



# coordinates:



# latitude: '37.4275'



# longitude: '-122.1697'



# directions: Enter Building 1 and take the stairs to Office 200 on Floor 2



# office_hours:



# - 'Monday 10:00 to 13:00'



# - 'Wednesday 09:00 to 10:00'



# appointment_url: '[https://calendly.com](https://calendly.com)'



# #contact_links:



# #  - icon: comments



# #    icon_pack: fas



# #    name: Discuss on Forum



# #    link: '[https://discourse.gohugo.io](https://discourse.gohugo.io)'



# # Automatically link email and phone or display as text?



# autolink: true



# # Email form provider



# form:



# provider: netlify



# formspree:



# id:



# netlify:



# # Enable CAPTCHA challenge to reduce spam?



# captcha: false



# design:



# columns: '1'



# spacing:



# padding: ["30px", "0px", "30px", "0px"]

---

