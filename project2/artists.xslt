<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:html="http://www.w3.org/1999/xhtml"
                xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
                xmlns:foaf="http://xmlns.com/foaf/spec/"
                xmlns:spot="http://artists.org/pred/">

    <xsl:template match="/">
    <rdf:RDF>
        <xsl:apply-templates/>
    </rdf:RDF>
    </xsl:template>


    <xsl:template match="item">
        <xsl:variable name="item"><xsl:value-of select="id"/></xsl:variable>
        <rdf:Description rdf:about="http://artists.org/{$item}">
            <foaf:name_artist><xsl:value-of select="name"/></foaf:name_artist>
            <spot:id><xsl:value-of select="id"/></spot:id>
            <spot:popularity><xsl:value-of select="popularity"/></spot:popularity>
            <spot:followers><xsl:value-of select="followers/total"/></spot:followers>
        </rdf:Description>
    </xsl:template>

</xsl:stylesheet>