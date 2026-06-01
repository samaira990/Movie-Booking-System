Task 3: Secure YouTube Trailer Embedding with Performance Controls

Objective:
The objective of this task was to integrate YouTube movie trailers into movie detail pages while maintaining security, performance optimization, and protection against malicious content injection.

Implementation Details:

1. Trailer URL Validation

* Implemented strict validation for trailer URLs.
* Only YouTube domains are accepted:

  * youtube.com
  * youtu.be
* Invalid URLs are rejected during movie creation or update.

Validation Logic:

* Custom model validation ensures only approved YouTube URLs are stored.
* Non-YouTube URLs trigger validation errors.

2. Secure Embed URL Generation

* Created a dedicated trailer_embed_url property.
* Extracts only the YouTube video ID.
* Generates safe embed URLs dynamically.

Example:
Input:
https://www.youtube.com/watch?v=VIDEO_ID

Generated:
https://www.youtube.com/embed/VIDEO_ID?rel=0

3. XSS Protection

* User-provided URLs are never directly rendered inside HTML.
* Only validated video IDs are used for iframe generation.
* Django template auto-escaping prevents malicious script execution.
* Direct JavaScript injection through trailer URLs is prevented.

Security Benefits:

* Prevents Cross-Site Scripting (XSS) attacks.
* Prevents malicious iframe source injection.
* Restricts external media sources to trusted YouTube domains only.

4. Trailer Embedding

* Embedded trailers directly on movie detail pages.
* Used responsive Bootstrap ratio containers for adaptive video display.
* Trailer section automatically appears only when a valid trailer exists.

5. Responsive Media Design

* Implemented Bootstrap responsive video containers.
* Videos automatically resize across:

  * Desktop
  * Tablet
  * Mobile Devices

6. Performance Optimization

* Trailer iframe loads only on movie detail pages.
* No unnecessary trailer requests are made on movie listing pages.
* Reduced bandwidth usage by avoiding autoplay functionality.
* Optimized embedded media loading for improved page speed.

7. Fallback Handling

* Implemented graceful fallback behavior.
* If trailer data is missing:

  * User sees "Trailer not available" message.
* Prevents broken iframe rendering.
* Ensures consistent user experience.

8. Error Handling
   Scenarios Handled:

* Missing trailer URL
* Invalid trailer URL
* Unsupported video source
* Removed or unavailable trailer links

9. Testing Performed

* Tested standard YouTube URLs.
* Tested shortened YouTube URLs.
* Tested invalid URLs.
* Tested missing trailer scenarios.
* Tested responsive behavior on multiple screen sizes.
* Verified iframe rendering and security restrictions.

Technologies Used:

* Django Models
* Django Validation Framework
* Bootstrap 5
* YouTube Embedded Player
* HTML5 iframe Integration

Security Measures Implemented:

* URL Validation
* Trusted Domain Restriction
* Dynamic Video ID Extraction
* Django Auto Escaping
* Controlled iframe Generation

Outcome:
The movie trailer system successfully embeds YouTube trailers while maintaining security, preventing XSS vulnerabilities, validating input URLs, handling missing trailers gracefully, and providing responsive media playback with minimal performance impact.
